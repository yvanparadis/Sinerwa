import httpx
from typing import List, Dict, Any, Optional
from app.core.config import get_settings
from app.integrations.base_adapter import ProviderAdapter


class TMDBAdapter(ProviderAdapter):
    def __init__(self):
        super().__init__("tmdb")
        self.settings = get_settings()
        self.base = self.settings.tmdb_base_url.rstrip("/")
        self.api_key = self.settings.tmdb_api_key
        self.access_token = self.settings.tmdb_access_token

    def is_authorized(self) -> bool:
        return bool(self.access_token or self.api_key)

    def _headers(self) -> dict:
        h = {}
        if self.access_token:
            h["Authorization"] = f"Bearer {self.access_token}"
        return h

    def _params(self, extra: Optional[dict] = None) -> dict:
        p = {}
        if not self.access_token and self.api_key:
            p["api_key"] = self.api_key
        if extra:
            p.update(extra)
        return p

    async def _get(self, path: str, params: Optional[dict] = None) -> Optional[Dict[str, Any]]:
        if not self.is_authorized():
            return None
        url = f"{self.base}{path}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(url, params=self._params(params), headers=self._headers())
                r.raise_for_status()
                return r.json()
            except Exception:
                return None

    async def fetch_listings(self) -> List[Dict[str, Any]]:
        collected: List[Dict[str, Any]] = []
        seen = set()
        for page in range(1, 6):
            for r in await self.popular(page):
                if r.get("id") not in seen:
                    seen.add(r.get("id"))
                    collected.append(r)
        for page in range(1, 4):
            for r in await self.top_rated(page):
                if r.get("id") not in seen:
                    seen.add(r.get("id"))
                    collected.append(r)
        for r in await self.now_playing(1):
            if r.get("id") not in seen:
                seen.add(r.get("id"))
                collected.append(r)
        for r in await self.upcoming(1):
            if r.get("id") not in seen:
                seen.add(r.get("id"))
                collected.append(r)
        for w in ("day", "week"):
            for r in await self.trending(w):
                if r.get("id") not in seen:
                    seen.add(r.get("id"))
                    collected.append(r)
        return collected

    async def fetch_metadata(self, external_id: str) -> Optional[Dict[str, Any]]:
        return await self._get(f"/movie/{external_id}")

    async def get_watch_link(self, external_id: str) -> Optional[str]:
        return None

    async def popular(self, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get("/movie/popular", {"page": page})
        return data.get("results", []) if data else []

    async def top_rated(self, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get("/movie/top_rated", {"page": page})
        return data.get("results", []) if data else []

    async def now_playing(self, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get("/movie/now_playing", {"page": page})
        return data.get("results", []) if data else []

    async def upcoming(self, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get("/movie/upcoming", {"page": page})
        return data.get("results", []) if data else []

    async def trending(self, window: str = "week") -> List[Dict[str, Any]]:
        data = await self._get(f"/trending/movie/{window}")
        return data.get("results", []) if data else []

    async def search(self, query: str, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get("/search/movie", {"query": query, "page": page})
        return data.get("results", []) if data else []

    async def details(self, movie_id: int) -> Optional[Dict[str, Any]]:
        return await self._get(f"/movie/{movie_id}", {"append_to_response": "credits,videos,similar"})

    async def genres(self) -> List[Dict[str, Any]]:
        data = await self._get("/genre/movie/list")
        return data.get("genres", []) if data else []

    async def similar(self, movie_id: int, page: int = 1) -> List[Dict[str, Any]]:
        data = await self._get(f"/movie/{movie_id}/similar", {"page": page})
        return data.get("results", []) if data else []
