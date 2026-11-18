from fastapi import APIRouter
from app.api.v1 import health, movies, providers, tmdb, local_media, storage, auth, watchlist, search, recommendations, genres, trailers, sitemap, admin

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(movies.router)
api_router.include_router(providers.router)
api_router.include_router(tmdb.router)
api_router.include_router(local_media.router)
api_router.include_router(storage.router)
api_router.include_router(auth.router)
api_router.include_router(watchlist.router)
api_router.include_router(search.router)
api_router.include_router(recommendations.router)
api_router.include_router(genres.router)
api_router.include_router(trailers.router)
api_router.include_router(sitemap.router)
api_router.include_router(admin.router)
