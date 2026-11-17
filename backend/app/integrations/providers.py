from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProviderStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    PENDING_AUTHORIZATION = "pending_authorization"
    ERROR = "error"


class AuthorizationStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    DENIED = "denied"


@dataclass
class ProviderInfo:
    id: str
    name: str
    website: str
    provider_type: str
    integration_method: str
    connection_status: str = ProviderStatus.DISCONNECTED.value
    authorization_status: str = AuthorizationStatus.PENDING.value
    api_available: bool = False
    last_sync_at: Optional[datetime] = None
    error_message: Optional[str] = None
    imported_count: int = 0


# Seed providers
PROVIDERS: Dict[str, ProviderInfo] = {
    "tmdb": ProviderInfo(
        id="tmdb",
        name="TMDB",
        website="https://www.themoviedb.org",
        provider_type="metadata",
        integration_method="api",
        connection_status=ProviderStatus.DISCONNECTED.value,
        authorization_status=AuthorizationStatus.AUTHORIZED.value,
        api_available=True,
    ),
    "oshakur_films": ProviderInfo(
        id="oshakur_films",
        name="OSHAkur Films",
        website="https://oshakurfilms.com",
        provider_type="streaming",
        integration_method="pending",
        connection_status=ProviderStatus.PENDING_AUTHORIZATION.value,
        authorization_status=AuthorizationStatus.PENDING.value,
        api_available=False,
    ),
    "agasobanuye_now": ProviderInfo(
        id="agasobanuye_now",
        name="Agasobanuye Now",
        website="https://agasobanuyenow.com",
        provider_type="streaming",
        integration_method="pending",
        connection_status=ProviderStatus.PENDING_AUTHORIZATION.value,
        authorization_status=AuthorizationStatus.PENDING.value,
        api_available=False,
    ),
    "local": ProviderInfo(
        id="local",
        name="CineRwa Local Storage",
        website="",
        provider_type="storage",
        integration_method="local_storage",
        connection_status=ProviderStatus.CONNECTED.value,
        authorization_status=AuthorizationStatus.AUTHORIZED.value,
        api_available=True,
    ),
}


def get_provider(provider_id: str) -> Optional[ProviderInfo]:
    return PROVIDERS.get(provider_id)


def list_providers() -> List[ProviderInfo]:
    return list(PROVIDERS.values())


def update_provider(provider_id: str, **kwargs) -> Optional[ProviderInfo]:
    p = PROVIDERS.get(provider_id)
    if not p:
        return None
    for k, v in kwargs.items():
        if hasattr(p, k):
            setattr(p, k, v)
    return p
