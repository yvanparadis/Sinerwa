from fastapi import APIRouter, Response
from app.services.sitemap_service import generate_sitemap

router = APIRouter(tags=["sitemap"])


@router.get("/sitemap.xml", response_class=Response)
def sitemap():
    return Response(content=generate_sitemap(), media_type="application/xml")
