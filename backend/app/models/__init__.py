from app.models.provider import (
    Provider,
    Movie,
    ExternalMovieIdentifier,
    MovieAvailability,
    SyncHistory,
    ContentRights,
    gen_uuid,
)
from app.models.user import User
from app.models.watchlist import WatchlistItem
from app.models.genre import Genre, movie_genres
from app.models.youtube_trailer import YouTubeTrailer
from app.models.intelligence import ClassificationHistory, ProcessingStatus
from app.models.audit_log import AuditLog

__all__ = [
    "Provider",
    "Movie",
    "ExternalMovieIdentifier",
    "MovieAvailability",
    "SyncHistory",
    "ContentRights",
    "gen_uuid",
    "User",
    "WatchlistItem",
    "Genre",
    "movie_genres",
    "YouTubeTrailer",
    "ClassificationHistory",
    "ProcessingStatus",
    "AuditLog",
]
