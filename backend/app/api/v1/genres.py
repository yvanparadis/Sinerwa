from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Genre, Movie
from app.services.genre_service import ensure_genres_from_tmdb, classify_all, classify_movie

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("")
def list_genres(db: Session = Depends(get_db)):
    ensure_genres_from_tmdb(db)
    rows = db.query(Genre).order_by(Genre.name).all()
    return {"genres": [{"id": g.id, "tmdb_id": g.tmdb_id, "name": g.name, "slug": g.slug} for g in rows]}


@router.get("/{genre_id}/movies")
def movies_by_genre(genre_id: str, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter((Genre.id == genre_id) | (Genre.slug == genre_id)).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    q = genre.movies
    total = len(q)
    page = q[offset:offset+limit]
    return {"genre": genre.name, "total": total, "items": [
        {"id": m.id, "title": m.title, "poster": m.poster, "rating": m.rating, "releaseDate": m.release_date,
         "playbackType": m.playback_type, "genres": [g.name for g in m.genre_links]} for m in page]}


@router.post("/classify-all")
def run_classification(db: Session = Depends(get_db)):
    result = classify_all(db)
    return result


@router.get("/unclassified")
def unclassified_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    unclassified = []
    for m in movies:
        if not m.genre_links:
            unclassified.append({"id": m.id, "title": m.title, "genres": m.genres})
    return {"count": len(unclassified), "items": unclassified}
