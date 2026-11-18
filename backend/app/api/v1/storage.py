import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header
from typing import Optional
from app.services.storage import get_storage_provider, storage_status
from app.services.gcs_storage import GCSStorageProvider
from app.core.config import get_settings

router = APIRouter(prefix="/storage", tags=["storage"])
settings = get_settings()

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")


def require_admin(x_admin_token: Optional[str] = Header(None)):
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=503, detail="Admin token not configured. Storage management disabled.")
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Admin authorization required.")


@router.get("/status")
def get_status():
    return storage_status()


@router.get("/gcs/status")
def gcs_status():
    p = GCSStorageProvider()
    return {
        "configured": p.configured(),
        "bucket": settings.gcs_bucket or None,
        "test": p.test_connection() if p.configured() else {"ok": False, "error": "Not configured"},
    }


@router.post("/test")
def test_connection(bucket: str, _: None = Depends(require_admin)):
    p = get_storage_provider()
    if bucket not in (settings.r2_private_bucket, settings.r2_public_bucket):
        raise HTTPException(status_code=400, detail="Unknown bucket.")
    return p.test_connection(bucket)


@router.get("/files")
def list_files(bucket: str, prefix: str = "", _: None = Depends(require_admin)):
    p = get_storage_provider()
    if bucket not in (settings.r2_private_bucket, settings.r2_public_bucket):
        raise HTTPException(status_code=400, detail="Unknown bucket.")
    try:
        return {"bucket": bucket, "files": p.list_files(bucket, prefix)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(
    bucket: str = Form(...),
    key: str = Form(...),
    file: UploadFile = File(...),
    _: None = Depends(require_admin),
):
    if bucket not in (settings.r2_private_bucket, settings.r2_public_bucket):
        raise HTTPException(status_code=400, detail="Unknown bucket.")
    # validate size
    data = await file.read()
    if len(data) > settings.r2_max_upload_bytes:
        raise HTTPException(status_code=413, detail="File exceeds max upload size.")
    # validate content type
    allowed = ("video/", "image/", "application/octet-stream")
    if not any((file.content_type or "").startswith(a) for a in allowed):
        raise HTTPException(status_code=415, detail="Unsupported file type.")
    p = get_storage_provider()
    try:
        res = p.upload_file(bucket, key, data, file.content_type or "application/octet-stream")
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/file")
def delete_file(bucket: str, key: str, _: None = Depends(require_admin)):
    if bucket not in (settings.r2_private_bucket, settings.r2_public_bucket):
        raise HTTPException(status_code=400, detail="Unknown bucket.")
    p = get_storage_provider()
    try:
        p.delete_file(bucket, key)
        return {"deleted": True, "bucket": bucket, "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/presign")
def presign(bucket: str, key: str, expires: int = 3600, _: None = Depends(require_admin)):
    if bucket not in (settings.r2_private_bucket, settings.r2_public_bucket):
        raise HTTPException(status_code=400, detail="Unknown bucket.")
    p = get_storage_provider()
    url = p.presigned_url(bucket, key, expires)
    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate signed URL.")
    return {"url": url, "expires_in": expires}
