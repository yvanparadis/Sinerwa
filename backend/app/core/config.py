from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "CineRwa API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./cinerwa.db"

    # JWT
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    @property
    def _secret_key_safe(self) -> str:
        if self.secret_key:
            return self.secret_key
        if self.debug:
            return "dev-only-insecure-secret-change-in-production"
        raise RuntimeError("SECRET_KEY must be set in production")

    # TMDB (never expose to frontend)
    tmdb_api_key: str = ""
    tmdb_access_token: str = ""
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    # YouTube Data API v3
    youtube_api_key: str = ""

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174", "https://cinerwa.vercel.app", "http://localhost:5175", "https://admin-cinerwa.vercel.app"]

    # Owner allowlist (comma-separated emails)
    owner_emails: str = ""

    # Cloudflare R2
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_private_bucket: str = ""
    r2_public_bucket: str = ""
    r2_s3_endpoint: str = ""
    r2_public_delivery_base_url: str = ""
    r2_max_upload_bytes: int = 100 * 1024 * 1024  # 100 MB default
    r2_warning_threshold_bytes: int = 9 * 1024 * 1024 * 1024  # 9 GB (free tier 10GB)

    # Google Cloud Storage
    gcs_project_id: str = ""
    gcs_bucket: str = ""
    gcs_credentials_json: str = ""  # path to service account JSON or inline
    gcs_public_delivery_base_url: str = ""

    # Backblaze B2
    b2_key_id: str = ""
    b2_application_key: str = ""
    b2_bucket: str = ""
    b2_endpoint: str = ""  # e.g. https://s3.us-west-004.backblazeb2.com
    b2_public_delivery_base_url: str = ""
    b2_max_upload_bytes: int = 5 * 1024 * 1024 * 1024  # 5 GB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
