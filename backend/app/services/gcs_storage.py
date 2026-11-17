import os
import json
import logging
from typing import Optional, Dict, Any, List
from app.core.config import get_settings

logger = logging.getLogger("cinerwa.gcs")

settings = get_settings()


class GCSStorageProvider:
    """Google Cloud Storage provider (REST-based, free-tier friendly)."""

    def configured(self) -> bool:
        return bool(settings.gcs_bucket and (settings.gcs_project_id or settings.gcs_credentials_json))

    def _access_token(self) -> Optional[str]:
        # If credentials_json is a file path or inline JSON, mint an OAuth token.
        cred = settings.gcs_credentials_json
        if not cred:
            return None
        try:
            if os.path.isfile(cred):
                with open(cred) as f:
                    data = json.load(f)
            else:
                data = json.loads(cred)
        except Exception:
            return None
        # Use google-auth if available
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request
            scopes = ["https://www.googleapis.com/auth/devstorage.read_write"]
            creds = service_account.Credentials.from_service_account_info(data, scopes=scopes)
            creds.refresh(Request())
            return creds.token
        except Exception as e:
            logger.warning("google-auth not available or failed: %s", e)
            return None

    def test_connection(self, bucket: Optional[str] = None) -> Dict[str, Any]:
        bucket = bucket or settings.gcs_bucket
        if not bucket:
            return {"ok": False, "error": "No bucket configured."}
        if not self.configured():
            return {"ok": False, "error": "GCS not configured."}
        token = self._access_token()
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        import httpx
        url = f"https://storage.googleapis.com/storage/v1/b/{bucket}"
        try:
            r = httpx.get(url, headers=headers, timeout=15.0)
            if r.status_code == 200:
                return {"ok": True, "bucket": bucket, "error": None}
            return {"ok": False, "bucket": bucket, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
        except Exception as e:
            return {"ok": False, "bucket": bucket, "error": str(e)}

    def list_files(self, prefix: str = "") -> List[Dict[str, Any]]:
        bucket = settings.gcs_bucket
        if not bucket:
            return []
        token = self._access_token()
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        import httpx
        url = f"https://storage.googleapis.com/storage/v1/b/{bucket}/o"
        params = {"maxResults": 1000}
        if prefix:
            params["prefix"] = prefix
        try:
            r = httpx.get(url, headers=headers, params=params, timeout=30.0)
            r.raise_for_status()
            data = r.json()
            out = []
            for it in data.get("items", []):
                out.append({
                    "key": it.get("name"),
                    "size": int(it.get("size", 0)),
                    "content_type": it.get("contentType"),
                    "updated": it.get("updated"),
                })
            return out
        except Exception as e:
            logger.error("GCS list failed: %s", e)
            return []

    def public_url(self, key: str) -> Optional[str]:
        base = settings.gcs_public_delivery_base_url
        if base:
            return f"{base.rstrip('/')}/{key}"
        if settings.gcs_bucket:
            return f"https://storage.googleapis.com/{settings.gcs_bucket}/{key}"
        return None
