from fastapi import APIRouter, HTTPException, Query
from app.integrations.tmdb_adapter import TMDBAdapter
from app.services.normalization import normalize

router = APIRouter(prefix="/tmdb", tags=["tmdb"])
adapter = TMDBAdapter()


@router.get("/popular")
async def popular(page: int = Query(1, ge=1)):
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB API key not configured")
    raw = await adapter.popular(page)
    return {"results": [normalize("tmdb", r) for r in raw]}


@router.get("/trending")
async def trending(window: str = Query("week", regex="^(day|week)$")):
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB API key not configured")
    raw = await adapter.trending(window)
    return {"results": [normalize("tmdb", r) for r in raw]}


@router.get("/search")
async def search(q: str = Query(..., min_length=1), page: int = Query(1, ge=1)):
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB API key not configured")
    raw = await adapter.search(q, page)
    return {"results": [normalize("tmdb", r) for r in raw]}


@router.get("/genres")
async def genres():
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB API key not configured")
    return {"genres": await adapter.genres()}


@router.get("/movie/{movie_id}")
async def movie_details(movie_id: int):
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB API key not configured")
    raw = await adapter.details(movie_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Movie not found")
    return normalize("tmdb", raw)
