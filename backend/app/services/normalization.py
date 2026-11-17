from typing import Dict, Any, Optional
from datetime import datetime


def normalize_tmdb(raw: Dict[str, Any], provider_id: str = "tmdb") -> Dict[str, Any]:
    genres = []
    if isinstance(raw.get("genres"), list):
        genres = [g.get("name") if isinstance(g, dict) else str(g) for g in raw["genres"]]
    elif isinstance(raw.get("genre_ids"), list):
        # leave ids; caller may map; keep as list of ids strings
        genres = [str(g) for g in raw["genre_ids"]]

    release = raw.get("release_date") or raw.get("first_air_date")
    poster_path = raw.get("poster_path")
    backdrop_path = raw.get("backdrop_path")
    base_img = "https://image.tmdb.org/t/p"

    return {
        "externalId": str(raw.get("id")) if raw.get("id") is not None else None,
        "title": raw.get("title") or raw.get("name") or "",
        "originalTitle": raw.get("original_title") or raw.get("original_name"),
        "overview": raw.get("overview") or "",
        "poster": f"{base_img}/w500{poster_path}" if poster_path else None,
        "backdrop": f"{base_img}/w1280{backdrop_path}" if backdrop_path else None,
        "releaseDate": release,
        "genres": genres,
        "language": raw.get("original_language"),
        "rating": raw.get("vote_average"),
        "runtime": raw.get("runtime"),
        "contentType": "movie",
        "providerId": provider_id,
        "externalWatchUrl": None,
        "playbackType": "external",
        "availabilityStatus": "metadata_only",
        "rightsStatus": "metadata_only",
        "metadataSource": provider_id,
    }


def normalize_curated(raw: Dict[str, Any], provider_id: str) -> Dict[str, Any]:
    return {
        "externalId": raw.get("externalId") or raw.get("external_id"),
        "title": raw.get("title", ""),
        "originalTitle": raw.get("originalTitle") or raw.get("original_title"),
        "overview": raw.get("overview", ""),
        "poster": raw.get("poster"),
        "backdrop": raw.get("backdrop"),
        "releaseDate": raw.get("releaseDate") or raw.get("release_date"),
        "genres": raw.get("genres", []),
        "language": raw.get("language"),
        "rating": raw.get("rating"),
        "runtime": raw.get("runtime"),
        "contentType": raw.get("contentType", "movie"),
        "providerId": provider_id,
        "externalWatchUrl": raw.get("externalWatchUrl") or raw.get("external_watch_url"),
        "playbackType": raw.get("playbackType", "external"),
        "availabilityStatus": raw.get("availabilityStatus", "available"),
        "rightsStatus": raw.get("rightsStatus", "unknown"),
        "metadataSource": provider_id,
        "translator": raw.get("translator"),
    }


def normalize(provider_id: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    if provider_id == "tmdb":
        return normalize_tmdb(raw, provider_id)
    return normalize_curated(raw, provider_id)
