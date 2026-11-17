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
]
