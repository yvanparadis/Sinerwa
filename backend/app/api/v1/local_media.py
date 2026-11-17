import os
import urllib.parse
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from app.services.local_library import _safe_root, scan_library

router = APIRouter(prefix="/local", tags=["local-library"])


def _resolve(rel: str) -> Path:
    base = _safe_root()
    # decode
    rel = urllib.parse.unquote(rel)
    target = (base / rel).resolve()
    # security: must be inside base
    try:
        target.relative_to(base)
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return target


@router.get("/library")
def local_library():
    return {"items": scan_library(), "root": str(_safe_root())}


@router.get("/media/{rel_path:path}")
def stream_media(rel_path: str, request: Request):
    target = _resolve(rel_path)
    # Range support
    file_size = target.stat().st_size
    range_header = request.headers.get("range")
    if range_header:
        # parse
        try:
            unit, rng = range_header.split("=", 1)
            start_str, end_str = rng.split("-", 1)
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
        except Exception:
            start, end = 0, file_size - 1
        if start >= file_size:
            raise HTTPException(status_code=416, detail="Range not satisfiable")
        end = min(end, file_size - 1)
        length = end - start + 1
        def iter_file():
            with open(target, "rb") as f:
                f.seek(start)
                remaining = length
                chunk = 65536
                while remaining > 0:
                    data = f.read(min(chunk, remaining))
                    if not data:
                        break
                    remaining -= len(data)
                    yield data
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
        }
        media_type = "video/mp4"
        # guess
        suf = target.suffix.lower()
        if suf == ".avi":
            media_type = "video/x-msvideo"
        elif suf == ".wmv":
            media_type = "video/x-ms-wmv"
        elif suf in (".mpg", ".mpeg"):
            media_type = "video/mpeg"
        elif suf == ".ts":
            media_type = "video/mp2t"
        return StreamingResponse(iter_file(), status_code=206, media_type=media_type, headers=headers)
    return FileResponse(target)
