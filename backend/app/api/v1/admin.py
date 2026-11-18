from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from app.core.database import get_db
from app.api.v1.auth import require_admin, get_current_user
from app.models import User, Movie, AuditLog

router = APIRouter(prefix="/admin", tags=["admin"])


class MovieCreate(BaseModel):
    title: str
    overview: Optional[str] = None
    poster: Optional[str] = None
    backdrop: Optional[str] = None
    releaseDate: Optional[str] = None
    genres: Optional[List[str]] = []
    language: Optional[str] = None
    rating: Optional[float] = None
    runtime: Optional[int] = None
    playbackType: Optional[str] = "METADATA_ONLY"
    availabilityStatus: Optional[str] = "unknown"
    externalWatchUrl: Optional[str] = None
    translator: Optional[str] = None


class MovieUpdate(MovieCreate):
    title: Optional[str] = None


def _audit(db, user, action, details=None):
    db.add(AuditLog(admin_id=user.id, action=action, details=details))
    db.commit()


@router.get("/overview")
def overview(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    from app.models import Genre, YouTubeTrailer
    total_movies = db.query(Movie).count()
    total_genres = db.query(Genre).count()
    recent = db.query(Movie).order_by(Movie.created_at.desc()).limit(5).all()
    missing_desc = db.query(Movie).filter(Movie.overview == None).count()
    missing_poster = db.query(Movie).filter(Movie.poster == None).count()
    no_trailer = db.query(Movie).count() - db.query(YouTubeTrailer).filter(YouTubeTrailer.is_primary == True).count()
    return {
        "total_movies": total_movies,
        "total_genres": total_genres,
        "movies_missing_description": missing_desc,
        "movies_missing_poster": missing_poster,
        "movies_without_trailer": no_trailer,
        "recent_movies": [{"id": m.id, "title": m.title, "createdAt": m.created_at.isoformat() if m.created_at else None} for m in recent],
    }


@router.get("/movies")
def admin_list_movies(q: str = None, limit: int = 50, offset: int = 0, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    query = db.query(Movie)
    if q:
        query = query.filter(Movie.title.ilike(f"%{q}%"))
    total = query.count()
    rows = query.order_by(Movie.created_at.desc()).offset(offset).limit(limit).all()
    return {"total": total, "items": [{"id": m.id, "title": m.title, "overview": m.overview, "poster": m.poster,
        "genres": m.genres or [], "language": m.language, "rating": m.rating, "runtime": m.runtime,
        "playbackType": m.playback_type, "availabilityStatus": m.availability_status, "providerId": m.provider_id,
        "createdAt": m.created_at.isoformat() if m.created_at else None} for m in rows]}


@router.post("/movies")
def create_movie(payload: MovieCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    m = Movie(
        title=payload.title,
        overview=payload.overview,
        poster=payload.poster,
        backdrop=payload.backdrop,
        release_date=payload.releaseDate,
        genres=payload.genres or [],
        language=payload.language,
        rating=payload.rating,
        runtime=payload.runtime,
        playback_type=payload.playbackType or "METADATA_ONLY",
        availability_status=payload.availabilityStatus or "unknown",
        external_watch_url=payload.externalWatchUrl,
        translator=payload.translator,
        metadata_source="admin",
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    _audit(db, current_user, "movie_created", f"Created movie {m.id}: {m.title}")
    return {"id": m.id, "title": m.title}


@router.put("/movies/{movie_id}")
def update_movie(movie_id: str, payload: MovieUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    m = db.query(Movie).filter(Movie.id == movie_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    for field, attr in [("title","title"),("overview","overview"),("poster","poster"),("backdrop","backdrop"),
                        ("releaseDate","release_date"),("genres","genres"),("language","language"),
                        ("rating","rating"),("runtime","runtime"),("playbackType","playback_type"),
                        ("availabilityStatus","availability_status"),("externalWatchUrl","external_watch_url"),
                        ("translator","translator")]:
        val = getattr(payload, field, None)
        if val is not None:
            setattr(m, attr, val)
    db.commit()
    _audit(db, current_user, "movie_updated", f"Updated movie {m.id}: {m.title}")
    return {"updated": True}


@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: str, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    m = db.query(Movie).filter(Movie.id == movie_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    title = m.title
    db.delete(m)
    db.commit()
    _audit(db, current_user, "movie_deleted", f"Deleted movie {movie_id}: {title}")
    return {"deleted": True}


@router.get("/audit-log")
def audit_log(limit: int = 50, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return {"items": [{"id": r.id, "admin_id": r.admin_id, "action": r.action, "details": r.details,
        "created_at": r.created_at.isoformat() if r.created_at else None} for r in rows]}


@router.get("/users")
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(User).all()
    return {"items": [{"id": u.id, "email": u.email, "username": u.username, "is_admin": u.is_admin,
        "is_active": u.is_active, "created_at": u.created_at.isoformat() if u.created_at else None} for u in rows]}


@router.get("/incomplete")
def incomplete_movies(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    rows = db.query(Movie).all()
    out = []
    for m in rows:
        issues = []
        if not m.overview: issues.append("missing description")
        if not m.poster: issues.append("missing poster")
        if not m.release_date: issues.append("missing release date")
        if not m.genres and not m.genre_links: issues.append("missing genres")
        if not m.language: issues.append("missing language")
        if issues:
            out.append({"id": m.id, "title": m.title, "issues": issues})
    return {"count": len(out), "items": out}
