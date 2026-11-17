import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Movie
from app.services.local_library import scan_library
from app.integrations.tmdb_adapter import TMDBAdapter
from app.core.config import get_settings


def _norm(s: Optional[str]) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s.lower().strip())


def _score(item: Dict[str, Any], q: str) -> int:
    q = _norm(q)
    if not q:
        return 0
    score = 0
    title = _norm(item.get("title"))
    overview = _norm(item.get("overview"))
    genres = " ".join(item.get("genres") or []).lower()
    translator = _norm(item.get("translator"))
    language = _norm(item.get("language"))
    # exact title match
    if title == q:
        score += 100
    if title.startswith(q):
        score += 60
    if q in title:
        score += 40
    # token overlap
    for tok in q.split():
        if tok in title:
            score += 15
        if tok in overview:
            score += 5
        if tok in genres:
            score += 10
        if tok in translator:
            score += 8
        if tok in language:
            score += 6
    # fuzzy: substring in overview
    if q in overview:
        score += 20
    return score


def search_all(db: Session, query: str, limit: int = 50) -> List[Dict[str, Any]]:
    q = query.strip()
    if not q:
        return []
    results: List[Dict[str, Any]] = []
    seen = set()

    # 1. DB movies
    for m in db.query(Movie).all():
        d = {
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
            "translator": m.translator,
            "source": m.metadata_source or "db",
        }
        if _score(d, q) > 0:
            key = (d["title"] or "").lower()
            if key not in seen:
                seen.add(key)
                d["_score"] = _score(d, q)
                results.append(d)

    # 2. Local library
    try:
        for it in scan_library():
            d = {
                "id": f"local:{it['path']}",
                "title": it["title"],
                "overview": f"Local media file: {it['path']}",
                "poster": "/placeholder-movie.svg",
                "backdrop": None,
                "releaseDate": None,
                "genres": ["Local"],
                "language": None,
                "rating": None,
                "runtime": None,
                "contentType": it.get("contentType", "movie"),
                "playbackType": "LOCAL_FILE",
                "availabilityStatus": "available",
                "translator": it.get("translator"),
                "source": "local",
            }
            if _score(d, q) > 0:
                key = (d["title"] or "").lower()
                if key not in seen:
                    seen.add(key)
                    d["_score"] = _score(d, q)
                    results.append(d)
    except Exception:
        pass

    # 3. TMDB (if configured)
    settings = get_settings()
    if settings.tmdb_api_key:
        raw = None
        try:
            adapter = TMDBAdapter()
            import asyncio
            loop = asyncio.new_event_loop()
            raw = loop.run_until_complete(adapter.search(q))
            loop.close()
        except Exception:
            raw = None
        if raw:
            for r in raw:
                from app.services.normalization import normalize_tmdb
                n = normalize_tmdb(r)
                d = {
                    "id": None,  # tmdb result not in db
                    "externalId": n.get("externalId"),
                    "title": n["title"],
                    "overview": n["overview"],
                    "poster": n["poster"],
                    "backdrop": n["backdrop"],
                    "releaseDate": n["releaseDate"],
                    "genres": n["genres"],
                    "language": n["language"],
                    "rating": n["rating"],
                    "runtime": n["runtime"],
                    "contentType": "movie",
                    "playbackType": "METADATA_ONLY",
                    "availabilityStatus": "metadata_only",
                    "translator": None,
                    "source": "tmdb",
                }
                if _score(d, q) > 0:
                    key = (d["title"] or "").lower()
                    if key not in seen:
                        seen.add(key)
                        d["_score"] = _score(d, q)
                        results.append(d)
    # sort by score desc, then title
    results.sort(key=lambda x: (-x.get("_score", 0), (x.get("title") or "")))
    for r in results:
        r.pop("_score", None)
    return results[:limit]
