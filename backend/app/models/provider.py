import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Provider(Base):
    __tablename__ = "providers"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    website = Column(String(256), nullable=True)
    provider_type = Column(String(64), nullable=False)  # metadata, streaming, aggregator
    integration_method = Column(String(64), nullable=False)  # api, feed, partner, manual
    connection_status = Column(String(32), default="disconnected")
    authorization_status = Column(String(32), default="pending")  # pending, authorized, denied
    api_available = Column(Boolean, default=False)
    last_sync_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    imported_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movies = relationship("Movie", back_populates="provider", lazy="dynamic")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(String(64), primary_key=True, default=gen_uuid)
    external_id = Column(String(128), nullable=True, index=True)
    title = Column(String(256), nullable=False, index=True)
    original_title = Column(String(256), nullable=True)
    overview = Column(Text, nullable=True)
    poster = Column(String(512), nullable=True)
    backdrop = Column(String(512), nullable=True)
    release_date = Column(String(32), nullable=True)
    genres = Column(JSON, default=list)
    language = Column(String(64), nullable=True)
    rating = Column(Float, nullable=True)
    runtime = Column(Integer, nullable=True)
    content_type = Column(String(32), default="movie")
    provider_id = Column(String(64), ForeignKey("providers.id"), nullable=True)
    external_watch_url = Column(String(512), nullable=True)
    playback_type = Column(String(32), default="external")
    availability_status = Column(String(32), default="unknown")
    rights_status = Column(String(32), default="unknown")
    metadata_source = Column(String(64), nullable=True)
    translator = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    provider = relationship("Provider", back_populates="movies")
    identifiers = relationship("ExternalMovieIdentifier", back_populates="movie", cascade="all, delete-orphan")
    availability = relationship("MovieAvailability", back_populates="movie", cascade="all, delete-orphan")
    genre_links = relationship("Genre", secondary="movie_genres", backref="movies")


class ExternalMovieIdentifier(Base):
    __tablename__ = "external_movie_identifiers"

    id = Column(String(64), primary_key=True, default=gen_uuid)
    movie_id = Column(String(64), ForeignKey("movies.id"), nullable=False)
    provider_id = Column(String(64), ForeignKey("providers.id"), nullable=False)
    external_id = Column(String(128), nullable=False, index=True)
    external_title = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie", back_populates="identifiers")


class MovieAvailability(Base):
    __tablename__ = "movie_availability"

    id = Column(String(64), primary_key=True, default=gen_uuid)
    movie_id = Column(String(64), ForeignKey("movies.id"), nullable=False)
    provider_id = Column(String(64), ForeignKey("providers.id"), nullable=False)
    status = Column(String(32), default="unknown")
    watch_url = Column(String(512), nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie", back_populates="availability")


class SyncHistory(Base):
    __tablename__ = "sync_history"

    id = Column(String(64), primary_key=True, default=gen_uuid)
    provider_id = Column(String(64), ForeignKey("providers.id"), nullable=False)
    status = Column(String(32), default="started")  # started, success, failed, skipped
    records_processed = Column(Integer, default=0)
    records_created = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_skipped = Column(Integer, default=0)
    duplicates_found = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)


class ContentRights(Base):
    __tablename__ = "content_rights"

    id = Column(String(64), primary_key=True, default=gen_uuid)
    movie_id = Column(String(64), ForeignKey("movies.id"), nullable=False)
    provider_id = Column(String(64), ForeignKey("providers.id"), nullable=False)
    rights_type = Column(String(64), nullable=False)  # metadata, streaming, embedding, link
    status = Column(String(32), default="pending")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
