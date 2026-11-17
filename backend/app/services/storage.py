import os
import logging
from typing import Optional, Dict, Any, List
from app.core.config import get_settings

logger = logging.getLogger("cinerwa.storage")

settings = get_settings()


class StorageProvider:
    """Abstract storage provider interface."""

    def configured(self) -> bool:
        raise NotImplementedError

    def test_connection(self, bucket: str) -> Dict[str, Any]:
        raise NotImplementedError

    def list_files(self, bucket: str, prefix: str = "") -> List[Dict[str, Any]]:
        raise NotImplementedError

    def upload_file(self, bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
        raise NotImplementedError

    def delete_file(self, bucket: str, key: str) -> bool:
        raise NotImplementedError

    def presigned_url(self, bucket: str, key: str, expires: int = 3600) -> Optional[str]:
        raise NotImplementedError

    def head_file(self, bucket: str, key: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError


class R2StorageProvider(StorageProvider):
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    def _endpoint(self) -> str:
        if self.settings.r2_s3_endpoint:
            return self.settings.r2_s3_endpoint
        if self.settings.r2_account_id:
            return f"https://{self.settings.r2_account_id}.r2.cloudflarestorage.com"
        return ""

    def configured(self) -> bool:
        return bool(
            self.settings.r2_access_key_id
            and self.settings.r2_secret_access_key
            and (self.settings.r2_account_id or self.settings.r2_s3_endpoint)
        )

    def _client_or_raise(self):
        if not self.configured():
            raise RuntimeError("R2 credentials are not configured.")
        if self._client is None:
            import boto3
            self._client = boto3.client(
                "s3",
                endpoint_url=self._endpoint(),
                aws_access_key_id=self.settings.r2_access_key_id,
                aws_secret_access_key=self.settings.r2_secret_access_key,
                region_name="auto",
            )
        return self._client

    def test_connection(self, bucket: str) -> Dict[str, Any]:
        try:
            client = self._client_or_raise()
            client.head_bucket(Bucket=bucket)
            # count objects (up to 1000)
            resp = client.list_objects_v2(Bucket=bucket, MaxKeys=1000)
            count = resp.get("KeyCount", 0)
            size = sum(o.get("Size", 0) for o in resp.get("Contents", []))
            return {"ok": True, "bucket": bucket, "file_count": count, "total_bytes": size, "error": None}
        except Exception as e:
            logger.error("R2 connection test failed for %s: %s", bucket, e)
            return {"ok": False, "bucket": bucket, "file_count": 0, "total_bytes": 0, "error": str(e)}

    def list_files(self, bucket: str, prefix: str = "") -> List[Dict[str, Any]]:
        client = self._client_or_raise()
        resp = client.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1000)
        out = []
        for o in resp.get("Contents", []):
            out.append({
                "key": o["Key"],
                "size": o.get("Size", 0),
                "last_modified": o.get("LastModified").isoformat() if o.get("LastModified") else None,
            })
        return out

    def upload_file(self, bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
        if len(data) > self.settings.r2_max_upload_bytes:
            raise ValueError(f"File exceeds max upload size of {self.settings.r2_max_upload_bytes} bytes.")
        client = self._client_or_raise()
        client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
        return {"bucket": bucket, "key": key, "size": len(data)}

    def delete_file(self, bucket: str, key: str) -> bool:
        client = self._client_or_raise()
        client.delete_object(Bucket=bucket, Key=key)
        return True

    def presigned_url(self, bucket: str, key: str, expires: int = 3600) -> Optional[str]:
        client = self._client_or_raise()
        try:
            return client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires,
            )
        except Exception as e:
            logger.error("presign failed: %s", e)
            return None

    def head_file(self, bucket: str, key: str) -> Optional[Dict[str, Any]]:
        client = self._client_or_raise()
        try:
            r = client.head_object(Bucket=bucket, Key=key)
            return {"size": r.get("ContentLength"), "content_type": r.get("ContentType")}
        except Exception:
            return None


# Singleton
_provider: Optional[StorageProvider] = None


def get_storage_provider() -> StorageProvider:
    global _provider
    if _provider is None:
        _provider = R2StorageProvider()
    return _provider


def storage_status() -> Dict[str, Any]:
    p = get_storage_provider()
    configured = p.configured()
    private_info = p.test_connection(settings.r2_private_bucket) if (configured and settings.r2_private_bucket) else {"ok": False, "error": "Not configured"}
    public_info = p.test_connection(settings.r2_public_bucket) if (configured and settings.r2_public_bucket) else {"ok": False, "error": "Not configured"}
    # warning thresholds
    warnings = []
    for info in (private_info, public_info):
        if info.get("ok") and info.get("total_bytes", 0) >= settings.r2_warning_threshold_bytes:
            warnings.append(f"Bucket {info['bucket']} approaching free-tier limit.")
    return {
        "configured": configured,
        "endpoint": p._endpoint() if configured else None,
        "private_bucket": settings.r2_private_bucket or None,
        "public_bucket": settings.r2_public_bucket or None,
        "private": private_info,
        "public": public_info,
        "max_upload_bytes": settings.r2_max_upload_bytes,
        "warnings": warnings,
    }
