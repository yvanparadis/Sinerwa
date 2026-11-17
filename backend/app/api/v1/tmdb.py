from fastapi import APIRouter, HTTPException, Query
from app.integrations.tmdb_adapter import TMDBAdapter
from app.services.normalization import normalize

router = APIRouter(prefix="/tmdb", tags=["tmdb"])
adapter = TMDBAdapter()


def _require():
    if not adapter.is_authorized():
        raise HTTPException(status_code=503, detail="TMDB credentials not configured")


@router.get("/popular")
async def popular(page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.popular(page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}


@router.get("/top_rated")
async def top_rated(page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.top_rated(page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}


@router.get("/now_playing")
async def now_playing(page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.now_playing(page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}


@router.get("/upcoming")
async def upcoming(page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.upcoming(page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}


@router.get("/trending")
async def trending(window: str = Query("week", pattern="^(day|week)$")):
    _require()
    raw = await adapter.trending(window)
    return {"results": [normalize("tmdb", r) for r in raw]}


@router.get("/search")
async def search(q: str = Query(..., min_length=1), page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.search(q, page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}


@router.get("/genres")
async def genres():
    _require()
    return {"genres": await adapter.genres()}


@router.get("/movie/{movie_id}")
async def movie_details(movie_id: int):
    _require()
    raw = await adapter.details(movie_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Movie not found")
    return normalize("tmdb", raw)


@router.get("/movie/{movie_id}/similar")
async def similar(movie_id: int, page: int = Query(1, ge=1)):
    _require()
    raw = await adapter.similar(movie_id, page)
    return {"results": [normalize("tmdb", r) for r in raw], "page": page}
