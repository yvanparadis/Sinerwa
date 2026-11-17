from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.search_service import search_all

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(q: str = Query(..., min_length=1), limit: int = Query(50, ge=1, le=200), db: Session = Depends(get_db)):
    results = search_all(db, q, limit)
    return {"query": q, "results": results, "total": len(results)}
