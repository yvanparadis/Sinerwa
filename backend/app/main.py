from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import Base, engine
from app.api.v1 import api_router
from app.models import Provider, User, WatchlistItem, YouTubeTrailer  # noqa: F401

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    # Seed provider registry
    from app.core.database import SessionLocal
    from app.models import Provider
    from app.integrations.providers import list_providers
    db = SessionLocal()
    try:
        for info in list_providers():
            if not db.query(Provider).filter(Provider.id == info.id).first():
                db.add(Provider(
                    id=info.id,
                    name=info.name,
                    website=info.website,
                    provider_type=info.provider_type,
                    integration_method=info.integration_method,
                    connection_status=info.connection_status,
                    authorization_status=info.authorization_status,
                    api_available=info.api_available,
                ))
        db.commit()
    finally:
        db.close()

    # Seed curated movie "Possible Love"
    from app.core.database import SessionLocal as _SL2
    from app.models import Movie
    s = _SL2()
    try:
        if not s.query(Movie).filter(Movie.title == "Possible Love").first():
            s.add(Movie(
                title="Possible Love",
                overview="A heartwarming story about the possibilities of love and connection.",
                poster="/placeholder-movie.svg",
                backdrop=None,
                release_date="2024-01-01",
                genres=["Romance", "Drama"],
                language="English",
                rating=9.0,
                runtime=120,
                content_type="movie",
                provider_id="local",
                playback_type="METADATA_ONLY",
                availability_status="unavailable",
                rights_status="unknown",
                metadata_source="curated",
            ))
            s.commit()
    finally:
        s.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"name": "CineRwa API", "version": settings.app_version, "docs": "/docs"}


app.include_router(api_router, prefix=settings.api_v1_prefix)
