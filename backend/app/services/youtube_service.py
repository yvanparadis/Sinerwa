import re
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models import YouTubeTrailer

settings = get_settings()

YT_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YT_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"

TRAILER_KEYWORDS = ["trailer", "official trailer", "teaser"]
BAD_KEYWORDS = ["reaction", "review", "fan edit", "compilation", "behind the scenes", "interview"]


def _configured() -> bool:
    return bool(settings.youtube_api_key)


def _score_result(item: Dict[str, Any], movie_title: str, year: Optional[str]) -> int:
    score = 0
    title = (item.get("snippet", {}).get("title") or "").lower()
    channel = (item.get("snippet", {}).get("channelTitle") or "").lower()
    desc = (item.get("snippet", {}).get("description") or "").lower()
    movie_l = (movie_title or "").lower()
    # title relevance
    if movie_l in title:
        score += 40
    for tok in movie_l.split():
        if tok in title:
            score += 8
    # trailer keywords
    for kw in TRAILER_KEYWORDS:
        if kw in title:
            score += 25
    # official channel boost
    if "official" in channel or "studio" in channel or "pictures" in channel or "films" in channel:
        score += 20
    # year match
    if year and year in title:
        score += 15
    # bad keywords penalty
    for bk in BAD_KEYWORDS:
        if bk in title or bk in desc:
            score -= 40
    # embeddable check later
    return score


def search_trailers(movie_title: str, year: Optional[str] = None, max_results: int = 8) -> List[Dict[str, Any]]:
    if not _configured():
        return []
    query = f"{movie_title} {year or ''} official trailer".strip()
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": settings.youtube_api_key,
        "videoEmbeddable": "true",
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get(YT_SEARCH_URL, params=params)
            r.raise_for_status()
            data = r.json()
    except Exception:
        return []
    items = []
    for it in data.get("items", []):
        vid = it.get("id", {}).get("videoId")
        if not vid:
            continue
        snippet = it.get("snippet", {})
        items.append({
            "video_id": vid,
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url") or snippet.get("thumbnails", {}).get("default", {}).get("url"),
            "published_at": snippet.get("publishedAt"),
            "score": _score_result(it, movie_title, year),
        })
    # validate embeddability
    if items:
        ids = ",".join(i["video_id"] for i in items)
        try:
            with httpx.Client(timeout=15.0) as client:
                r = client.get(YT_VIDEOS_URL, params={"part": "status,contentDetails,snippet", "id": ids, "key": settings.youtube_api_key})
                r.raise_for_status()
                vdata = r.json()
            vmap = {v["id"]: v for v in vdata.get("items", [])}
            for it in items:
                v = vmap.get(it["video_id"])
                if v:
                    status = v.get("status", {})
                    it["embeddable"] = status.get("embeddable", False)
                    it["privacy"] = status.get("privacyStatus")
                    it["duration"] = v.get("contentDetails", {}).get("duration")
                    if not it["embeddable"]:
                        it["score"] -= 50
                    if it["privacy"] != "public":
                        it["score"] -= 100
                else:
                    it["embeddable"] = False
                    it["score"] -= 100
        except Exception:
            pass
    items.sort(key=lambda x: -x["score"])
    return items


def discover_trailer(movie_title: str, year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    results = search_trailers(movie_title, year)
    if not results:
        return None
    best = results[0]
    if best["score"] < 20:
        return None
    best["video_url"] = f"https://www.youtube.com/watch?v={best['video_id']}"
    best["embed_url"] = f"https://www.youtube.com/embed/{best['video_id']}"
    return best


def save_trailer(db: Session, movie_id: str, trailer: Optional[Dict[str, Any]], language: Optional[str] = None) -> YouTubeTrailer:
    # remove existing primary? keep history; mark new as primary
    existing = db.query(YouTubeTrailer).filter(YouTubeTrailer.movie_id == movie_id, YouTubeTrailer.is_primary == True).all()
    for e in existing:
        e.is_primary = False
    if trailer is None:
        rec = YouTubeTrailer(movie_id=movie_id, video_id="", verification_status="not_found", is_primary=True)
    else:
        rec = YouTubeTrailer(
            movie_id=movie_id,
            video_id=trailer["video_id"],
            video_title=trailer.get("title"),
            channel_name=trailer.get("channel"),
            thumbnail_url=trailer.get("thumbnail"),
            video_url=trailer.get("video_url"),
            embed_url=trailer.get("embed_url"),
            language=language,
            trailer_type="trailer",
            verification_status="verified" if trailer.get("score", 0) >= 40 else "pending",
            is_primary=True,
        )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def get_primary_trailer(db: Session, movie_id: str) -> Optional[YouTubeTrailer]:
    return db.query(YouTubeTrailer).filter(YouTubeTrailer.movie_id == movie_id, YouTubeTrailer.is_primary == True).first()


def discover_for_movie(db: Session, movie_title: str, year: Optional[str] = None, language: Optional[str] = None, movie_id: Optional[str] = None) -> YouTubeTrailer:
    mid = movie_id or movie_title
    trailer = discover_trailer(movie_title, year)
    return save_trailer(db, mid, trailer, language)
