from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models import User, WatchlistItem, Movie
from app.api.v1.auth import get_current_user as _gcu

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("")
def list_watchlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id).all()
    ids = [r.movie_id for r in rows]
    movies = []
    for mid in ids:
        m = db.query(Movie).filter(Movie.id == mid).first()
        if m:
            movies.append({
                "id": m.id, "title": m.title, "poster": m.poster, "backdrop": m.backdrop,
                "rating": m.rating, "releaseDate": m.release_date, "genres": m.genres or [],
                "playbackType": m.playback_type, "translator": m.translator,
            })
    return {"items": movies}


@router.post("/{movie_id}")
def add_to_watchlist(movie_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id, WatchlistItem.movie_id == movie_id).first()
    if existing:
        return {"added": False, "message": "Already in watchlist"}
    db.add(WatchlistItem(user_id=current_user.id, movie_id=movie_id))
    db.commit()
    return {"added": True}


@router.delete("/{movie_id}")
def remove_from_watchlist(movie_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id, WatchlistItem.movie_id == movie_id).first()
    if row:
        db.delete(row)
        db.commit()
        return {"removed": True}
    return {"removed": False}
