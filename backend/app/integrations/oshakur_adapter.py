from app.integrations.base_adapter import ProviderAdapter
from typing import List, Dict, Any, Optional


class OshakurFilmsAdapter(ProviderAdapter):
    def __init__(self):
        super().__init__("oshakur_films")

    def is_authorized(self) -> bool:
        return False

    async def fetch_listings(self) -> List[Dict[str, Any]]:
        # Authorization pending. No automated harvesting.
        return []

    async def fetch_metadata(self, external_id: str) -> Optional[Dict[str, Any]]:
        return None

    async def get_watch_link(self, external_id: str) -> Optional[str]:
        return None
