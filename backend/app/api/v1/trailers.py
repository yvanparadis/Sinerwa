from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.youtube_service import discover_for_movie, get_primary_trailer, search_trailers
from app.models import YouTubeTrailer
from datetime import datetime

router = APIRouter(prefix="/trailers", tags=["trailers"])


@router.get("/search")
def search_trailers_endpoint(q: str = Query(...), year: str = Query(None), db: Session = Depends(get_db)):
    results = search_trailers(q, year)
    return {"query": q, "results": results}


@router.post("/discover")
def discover(movie_title: str = Query(...), year: str = Query(None), language: str = Query(None), movie_id: str = Query(None), db: Session = Depends(get_db)):
    mid = movie_id or movie_title
    t = discover_for_movie(db, mid, year, language, mid)
    if not t.video_id:
        return {"movie_id": mid, "status": "not_found", "trailer": None}
    return {
        "movie_id": mid,
        "status": t.verification_status,
        "trailer": {
            "video_id": t.video_id,
            "title": t.video_title,
            "channel": t.channel_name,
            "thumbnail": t.thumbnail_url,
            "url": t.video_url,
            "embed_url": t.embed_url,
        },
    }


@router.get("/{movie_id}")
def get_trailer(movie_id: str, db: Session = Depends(get_db)):
    t = get_primary_trailer(db, movie_id)
    if not t or not t.video_id:
        return {"movie_id": movie_id, "status": "not_found", "trailer": None}
    return {
        "movie_id": movie_id,
        "status": t.verification_status,
        "trailer": {
            "video_id": t.video_id,
            "title": t.video_title,
            "channel": t.channel_name,
            "thumbnail": t.thumbnail_url,
            "url": t.video_url,
            "embed_url": t.embed_url,
            "language": t.language,
        },
    }


@router.post("/{movie_id}/verify")
def verify(movie_id: str, video_id: str = Query(...), db: Session = Depends(get_db)):
    t = db.query(YouTubeTrailer).filter(YouTubeTrailer.movie_id == movie_id, YouTubeTrailer.video_id == video_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Trailer not found")
    t.verification_status = "verified"
    t.last_checked = datetime.utcnow()
    db.commit()
    return {"verified": True}


@router.delete("/{movie_id}")
def remove_trailer(movie_id: str, db: Session = Depends(get_db)):
    db.query(YouTubeTrailer).filter(YouTubeTrailer.movie_id == movie_id).delete()
    db.commit()
    return {"removed": True}
