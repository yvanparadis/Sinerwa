from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Movie
from app.services.local_library import scan_library
from app.services.normalization import normalize

router = APIRouter(prefix="/movies", tags=["movies"])


def _local_items():
    try:
        raws = scan_library()
    except Exception:
        return []
    out = []
    for r in raws:
        n = normalize("local", {
            "externalId": r["path"],
            "title": r["title"],
            "overview": f"Local media file: {r['path']}",
            "poster": "/placeholder-movie.svg",
            "backdrop": None,
            "releaseDate": None,
            "genres": ["Local"],
            "language": None,
            "rating": None,
            "runtime": None,
            "contentType": r.get("contentType", "movie"),
            "externalWatchUrl": r["url"],
            "playbackType": "LOCAL_FILE",
            "availabilityStatus": "available",
            "rightsStatus": "owned",
            "metadataSource": "local",
            "translator": r.get("translator"),
        })
        n["id"] = f"local:{r['path']}"
        out.append(n)
    return out


@router.get("")
def list_movies(db: Session = Depends(get_db)):
    rows = db.query(Movie).order_by(Movie.created_at.desc()).all()
    items = []
    seen = set()
    for m in rows:
        key = (m.title or "").strip().lower()
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "id": m.id,
            "title": m.title,
            "overview": m.overview,
            "poster": m.poster,
            "backdrop": m.backdrop,
            "releaseDate": m.release_date,
            "genres": m.genres or [],
            "language": m.language,
            "rating": m.rating,
            "runtime": m.runtime,
            "contentType": m.content_type,
            "source": m.metadata_source or "db",
            "playbackType": m.playback_type,
            "availabilityStatus": m.availability_status,
            "providerId": m.provider_id,
            "externalWatchUrl": m.external_watch_url,
            "translator": m.translator,
            "createdAt": m.created_at.isoformat() if m.created_at else None,
        })
    # Merge local library (avoid duplicates by title)
    for li in _local_items():
        key = (li.get("title") or "").strip().lower()
        if key in seen:
            continue
        seen.add(key)
        items.append({
            "id": li["id"],
            "title": li["title"],
            "overview": li["overview"],
            "poster": li["poster"],
            "backdrop": li["backdrop"],
            "releaseDate": li["releaseDate"],
            "genres": li["genres"] or [],
            "language": li["language"],
            "rating": li["rating"],
            "runtime": li["runtime"],
            "contentType": li["contentType"],
            "source": li["metadataSource"],
            "playbackType": li["playbackType"],
            "availabilityStatus": li["availabilityStatus"],
            "providerId": li["providerId"],
            "externalWatchUrl": li["externalWatchUrl"],
            "translator": li["translator"],
            "createdAt": None,
        })
    return {"items": items, "total": len(items)}


@router.get("/{movie_id:path}")
def get_movie(movie_id: str, db: Session = Depends(get_db)):
    if movie_id.startswith("local:"):
        rel = movie_id[len("local:"):]
        for li in _local_items():
            if li["externalId"] == rel or li["id"] == movie_id:
                return {
                    "id": li["id"],
                    "title": li["title"],
                    "overview": li["overview"],
                    "poster": li["poster"],
                    "backdrop": li["backdrop"],
                    "releaseDate": li["releaseDate"],
                    "genres": li["genres"] or [],
                    "language": li["language"],
                    "rating": li["rating"],
                    "runtime": li["runtime"],
                    "contentType": li["contentType"],
                    "source": li["metadataSource"],
                    "playbackType": li["playbackType"],
                    "availabilityStatus": li["availabilityStatus"],
                    "providerId": li["providerId"],
                    "externalWatchUrl": li["externalWatchUrl"],
                    "translator": li["translator"],
                }
        raise HTTPException(status_code=404, detail="Movie not found")
    m = db.query(Movie).filter(Movie.id == movie_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {
        "id": m.id,
        "title": m.title,
        "overview": m.overview,
        "poster": m.poster,
        "backdrop": m.backdrop,
        "releaseDate": m.release_date,
        "genres": m.genres or [],
        "language": m.language,
        "rating": m.rating,
        "runtime": m.runtime,
        "contentType": m.content_type,
        "source": m.metadata_source or "db",
        "playbackType": m.playback_type,
        "availabilityStatus": m.availability_status,
        "providerId": m.provider_id,
        "externalWatchUrl": m.external_watch_url,
        "translator": m.translator,
    }
