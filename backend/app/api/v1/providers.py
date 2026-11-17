from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Provider, SyncHistory
from app.integrations.providers import list_providers, get_provider
from app.services.sync_engine import sync_provider, ensure_provider_row

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
def list_provider_status(db: Session = Depends(get_db)):
    result = []
    for info in list_providers():
        ensure_provider_row(db, info.id)
    rows = db.query(Provider).all()
    for r in rows:
        info = get_provider(r.id)
        result.append({
            "id": r.id,
            "name": r.name,
            "website": r.website,
            "provider_type": r.provider_type,
            "integration_method": r.integration_method,
            "connection_status": r.connection_status,
            "authorization_status": r.authorization_status,
            "api_available": r.api_available,
            "last_sync_at": r.last_sync_at.isoformat() if r.last_sync_at else None,
            "imported_count": r.imported_count,
            "error_message": r.error_message,
        })
    return {"providers": result}


@router.get("/{provider_id}")
def get_provider_status(provider_id: str, db: Session = Depends(get_db)):
    row = db.query(Provider).filter(Provider.id == provider_id).first()
    if not row:
        ensure_provider_row(db, provider_id)
        row = db.query(Provider).filter(Provider.id == provider_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Provider not found")
    return {
        "id": row.id,
        "name": row.name,
        "website": row.website,
        "provider_type": row.provider_type,
        "integration_method": row.integration_method,
        "connection_status": row.connection_status,
        "authorization_status": row.authorization_status,
        "api_available": row.api_available,
        "last_sync_at": row.last_sync_at.isoformat() if row.last_sync_at else None,
        "imported_count": row.imported_count,
        "error_message": row.error_message,
    }


@router.post("/{provider_id}/sync")
async def trigger_sync(provider_id: str, db: Session = Depends(get_db)):
    if provider_id not in [p.id for p in list_providers()]:
        raise HTTPException(status_code=404, detail="Unknown provider")
    history = await sync_provider(db, provider_id)
    added = history.records_created or 0
    updated = history.records_updated or 0
    skipped = history.records_skipped or 0
    failed = history.records_failed or 0
    if history.status == "skipped":
        message = history.error_message or "No synchronization performed."
    elif added == 0 and updated == 0:
        message = "No new movies found."
    elif failed > 0:
        message = f"Synchronization completed with errors: {added} added, {updated} updated, {skipped} skipped, {failed} failed."
    else:
        message = f"Synchronization successful: {added} added, {updated} updated, {skipped} skipped."
    return {
        "id": history.id,
        "provider_id": history.provider_id,
        "status": history.status,
        "message": message,
        "records_processed": history.records_processed or 0,
        "records_added": added,
        "records_updated": updated,
        "records_skipped": skipped,
        "records_failed": failed,
        "error_message": history.error_message,
        "last_sync_at": history.finished_at.isoformat() if history.finished_at else None,
    }


@router.get("/{provider_id}/sync-history")
def sync_history(provider_id: str, db: Session = Depends(get_db)):
    rows = db.query(SyncHistory).filter(SyncHistory.provider_id == provider_id).order_by(SyncHistory.started_at.desc()).limit(50).all()
    return {
        "history": [
            {
                "id": r.id,
                "status": r.status,
                "records_processed": r.records_processed,
                "records_created": r.records_created,
                "duplicates_found": r.records_created and r.duplicates_found,
                "error_message": r.error_message,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            }
            for r in rows
        ]
    }
