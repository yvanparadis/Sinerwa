from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Provider, Movie, ExternalMovieIdentifier, SyncHistory
from app.integrations.providers import get_provider, list_providers
from app.integrations.base_adapter import ProviderAdapter
from app.integrations.oshakur_adapter import OshakurFilmsAdapter
from app.integrations.agasobanuye_adapter import AgasobanuyeNowAdapter
from app.integrations.tmdb_adapter import TMDBAdapter
from app.integrations.local_adapter import LocalStorageAdapter
from app.services.normalization import normalize

ADAPTERS = {
    "oshakur_films": OshakurFilmsAdapter,
    "agasobanuye_now": AgasobanuyeNowAdapter,
    "tmdb": TMDBAdapter,
    "local": LocalStorageAdapter,
}


def get_adapter(provider_id: str) -> ProviderAdapter:
    cls = ADAPTERS.get(provider_id)
    if not cls:
        raise ValueError(f"No adapter for provider {provider_id}")
    return cls()


def ensure_provider_row(db: Session, provider_id: str):
    from app.integrations.providers import get_provider as gp
    info = gp(provider_id)
    row = db.query(Provider).filter(Provider.id == provider_id).first()
    if not row:
        row = Provider(
            id=provider_id,
            name=info.name,
            website=info.website,
            provider_type=info.provider_type,
            integration_method=info.integration_method,
            connection_status=info.connection_status,
            authorization_status=info.authorization_status,
            api_available=info.api_available,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


async def sync_provider(db: Session, provider_id: str) -> SyncHistory:
    from app.integrations.providers import get_provider as gp
    info = gp(provider_id)
    row = ensure_provider_row(db, provider_id)
    history = SyncHistory(provider_id=provider_id, status="started")
    db.add(history)
    db.commit()
    db.refresh(history)

    # Authorization gate
    if info.authorization_status != "authorized":
        history.status = "skipped"
        history.error_message = (
            f"Provider '{info.name}' is not authorized. "
            "No catalog changes made. Authorization and an approved integration method are required."
        )
        history.finished_at = datetime.utcnow()
        row.connection_status = "pending_authorization"
        row.error_message = history.error_message
        db.commit()
        return history

    if not info.api_available:
        history.status = "skipped"
        history.error_message = f"Provider '{info.name}' has no available API."
        history.finished_at = datetime.utcnow()
        row.connection_status = "disconnected"
        row.error_message = history.error_message
        db.commit()
        return history

    adapter = get_adapter(provider_id)
    if not adapter.is_authorized():
        history.status = "skipped"
        history.error_message = (
            f"Provider '{info.name}' adapter is not authorized (missing credentials). "
            "Configure credentials in backend environment."
        )
        history.finished_at = datetime.utcnow()
        row.connection_status = "disconnected"
        row.error_message = history.error_message
        db.commit()
        return history

    processed = 0
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    errors = []

    try:
        raw_listings = await adapter.fetch_listings()
    except Exception as e:
        history.status = "failed"
        history.error_message = f"Failed to fetch listings: {e}"
        history.finished_at = datetime.utcnow()
        row.connection_status = "error"
        row.error_message = history.error_message
        db.commit()
        return history

    for raw in (raw_listings or []):
        processed += 1
        try:
            norm = normalize(provider_id, raw)
            title = norm.get("title", "")
            ext_id = norm.get("externalId")
            # Find existing by external id + provider
            existing = None
            if ext_id:
                existing = db.query(Movie).filter(
                    Movie.external_id == ext_id, Movie.provider_id == provider_id
                ).first()
            if existing:
                # update
                existing.title = norm.get("title", existing.title)
                existing.original_title = norm.get("originalTitle", existing.original_title)
                existing.overview = norm.get("overview", existing.overview)
                existing.poster = norm.get("poster", existing.poster)
                existing.backdrop = norm.get("backdrop", existing.backdrop)
                existing.release_date = norm.get("releaseDate", existing.release_date)
                existing.genres = norm.get("genres", existing.genres)
                existing.language = norm.get("language", existing.language)
                existing.rating = norm.get("rating", existing.rating)
                existing.runtime = norm.get("runtime", existing.runtime)
                existing.availability_status = norm.get("availabilityStatus", existing.availability_status)
                existing.rights_status = norm.get("rightsStatus", existing.rights_status)
                existing.metadata_source = norm.get("metadataSource", existing.metadata_source)
                existing.updated_at = datetime.utcnow()
                updated += 1
                continue
            # duplicate by title+year across providers?
            from app.services.dedup import is_duplicate
            existing_dicts = [
                {"externalId": m.external_id, "title": m.title, "releaseDate": m.release_date, "providerId": m.provider_id}
                for m in db.query(Movie).all()
            ]
            if any(is_duplicate(norm, d) for d in existing_dicts):
                skipped += 1
                continue
            # insert
            movie = Movie(
                external_id=ext_id,
                title=title,
                original_title=norm.get("originalTitle"),
                overview=norm.get("overview"),
                poster=norm.get("poster"),
                backdrop=norm.get("backdrop"),
                release_date=norm.get("releaseDate"),
                genres=norm.get("genres", []),
                language=norm.get("language"),
                rating=norm.get("rating"),
                runtime=norm.get("runtime"),
                content_type=norm.get("contentType", "movie"),
                provider_id=provider_id,
                external_watch_url=norm.get("externalWatchUrl"),
                playback_type=norm.get("playbackType", "external"),
                availability_status=norm.get("availabilityStatus", "unknown"),
                rights_status=norm.get("rightsStatus", "unknown"),
                metadata_source=norm.get("metadataSource"),
                translator=norm.get("translator"),
            )
            db.add(movie)
            db.flush()
            if ext_id:
                db.add(ExternalMovieIdentifier(
                    movie_id=movie.id,
                    provider_id=provider_id,
                    external_id=ext_id,
                    external_title=title,
                ))
            created += 1
        except Exception as e:
            failed += 1
            errors.append(str(e))
            db.rollback()

    try:
        row.imported_count = (row.imported_count or 0) + created
        row.last_sync_at = datetime.utcnow()
        if failed and not (created or updated):
            row.connection_status = "error"
        else:
            row.connection_status = "connected"
        row.error_message = "; ".join(errors) if errors else None
        history.status = "success" if failed == 0 else "partial"
        history.records_processed = processed
        history.records_created = created
        history.records_updated = updated
        history.records_skipped = skipped
        history.duplicates_found = skipped
        history.records_failed = failed
        history.error_message = "; ".join(errors) if errors else None
        history.finished_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        history.status = "failed"
        history.error_message = str(e)
        history.finished_at = datetime.utcnow()
        row.connection_status = "error"
        row.error_message = str(e)
        db.commit()

    return history
