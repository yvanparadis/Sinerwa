from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class ProviderAdapter(ABC):
    def __init__(self, provider_id: str):
        self.provider_id = provider_id

    @abstractmethod
    async def fetch_listings(self) -> List[Dict[str, Any]]:
        """Fetch authorized movie listings. Return normalized-ready raw records."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_metadata(self, external_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get_watch_link(self, external_id: str) -> Optional[str]:
        raise NotImplementedError

    async def check_availability(self, external_id: str) -> str:
        return "unknown"

    def is_authorized(self) -> bool:
        return False
