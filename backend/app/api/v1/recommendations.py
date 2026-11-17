from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Movie, WatchlistItem, User
from app.api.v1.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import get_settings

router = APIRouter(prefix="/recommendations", tags=["recommendations"])
settings = get_settings()
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def _optional_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    if not token:
        return None
    try:
        from app.core.security import decode_token
        subject = decode_token(token)
        if not subject:
            return None
        return db.query(User).filter(User.id == subject).first()
    except Exception:
        return None


@router.get("")
def recommendations(limit: int = 12, current_user: User = Depends(_optional_user), db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        return {"items": []}
    # Build genre preference from watchlist
    preferred_genres = set()
    if current_user:
        wl = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id).all()
        for w in wl:
            m = db.query(Movie).filter(Movie.id == w.movie_id).first()
            if m and m.genres:
                for g in m.genres:
                    preferred_genres.add(g)
    # If no preferences, use top genres from all movies
    if not preferred_genres:
        from collections import Counter
        c = Counter()
        for m in movies:
            for g in (m.genres or []):
                c[g] += 1
        preferred_genres = set([g for g, _ in c.most_common(5)])

    scored = []
    for m in movies:
        score = m.rating or 0
        if m.genres:
            overlap = len(set(m.genres) & preferred_genres)
            score += overlap * 2
        scored.append((score, m))
    scored.sort(key=lambda x: -x[0])
    out = []
    for _, m in scored[:limit]:
        out.append({
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
            "playbackType": m.playback_type,
            "availabilityStatus": m.availability_status,
            "providerId": m.provider_id,
            "externalWatchUrl": m.external_watch_url,
            "translator": m.translator,
        })
    return {"items": out}
