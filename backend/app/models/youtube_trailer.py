import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, UniqueConstraint
from app.core.database import Base


class YouTubeTrailer(Base):
    __tablename__ = "youtube_trailers"
    __table_args__ = (UniqueConstraint("movie_id", "video_id", name="uq_movie_video"),)

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    movie_id = Column(String(128), nullable=False, index=True)
    video_id = Column(String(32), nullable=False, index=True)
    video_title = Column(String(256), nullable=True)
    channel_name = Column(String(256), nullable=True)
    thumbnail_url = Column(String(512), nullable=True)
    video_url = Column(String(512), nullable=True)
    embed_url = Column(String(512), nullable=True)
    language = Column(String(16), nullable=True)
    trailer_type = Column(String(32), default="trailer")
    verification_status = Column(String(32), default="pending")  # verified, pending, not_found, invalid
    discovered_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)
    is_primary = Column(Boolean, default=True)
