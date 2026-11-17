from typing import List, Dict, Any, Optional
from app.integrations.base_adapter import ProviderAdapter
from app.services.local_library import scan_library


class LocalStorageAdapter(ProviderAdapter):
    def __init__(self, root: Optional[str] = None):
        super().__init__("local")
        self.root = root

    def is_authorized(self) -> bool:
        return True

    async def fetch_listings(self) -> List[Dict[str, Any]]:
        items = scan_library(self.root)
        out = []
        for it in items:
            out.append({
                "externalId": it["path"],
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
                "providerId": "local",
                "externalWatchUrl": it["url"],
                "playbackType": "LOCAL_FILE",
                "availabilityStatus": "available",
                "rightsStatus": "owned",
                "metadataSource": "local",
                "translator": it.get("translator"),
                "subtitleUrl": it.get("subtitleUrl"),
            })
        return out

    async def fetch_metadata(self, external_id: str) -> Optional[Dict[str, Any]]:
        return None

    async def get_watch_link(self, external_id: str) -> Optional[str]:
        return f"/api/v1/local/media/{external_id}"
