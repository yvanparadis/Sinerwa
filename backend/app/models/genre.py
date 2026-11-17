import uuid
from sqlalchemy import Column, String, Table, ForeignKey, Integer
from app.core.database import Base

movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", String(64), ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", String(64), ForeignKey("genres.id"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tmdb_id = Column(Integer, unique=True, nullable=True, index=True)
    name = Column(String(64), unique=True, nullable=False, index=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
