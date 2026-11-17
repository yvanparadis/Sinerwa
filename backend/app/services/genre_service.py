from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Genre, Movie
from app.integrations.tmdb_adapter import TMDBAdapter

# TMDB genre id -> name (fallback if API unavailable)
TMDB_GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    53: "Thriller", 10752: "War", 37: "Western", 10402: "Musical",
}


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("&", "and")


def ensure_genres_from_tmdb(db: Session) -> List[Genre]:
    adapter = TMDBAdapter()
    # Try API
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        raw = loop.run_until_complete(adapter.genres())
        loop.close()
    except Exception:
        raw = []
    if raw:
        for g in raw:
            gid = g.get("id")
            name = g.get("name")
            if not name:
                continue
            existing = db.query(Genre).filter(Genre.tmdb_id == gid).first() or db.query(Genre).filter(Genre.name == name).first()
            if not existing:
                db.add(Genre(tmdb_id=gid, name=name, slug=slugify(name)))
            else:
                if existing.tmdb_id is None:
                    existing.tmdb_id = gid
        db.commit()
    # Ensure fallback genres exist
    for tid, name in TMDB_GENRE_MAP.items():
        existing = db.query(Genre).filter(Genre.tmdb_id == tid).first() or db.query(Genre).filter(Genre.name == name).first()
        if not existing:
            db.add(Genre(tmdb_id=tid, name=name, slug=slugify(name)))
        elif existing.tmdb_id is None:
            existing.tmdb_id = tid
    db.commit()
    return db.query(Genre).all()


def classify_movie(db: Session, movie: Movie) -> bool:
    """Assign genres to a movie based on its genres field (names or TMDB ids). Returns True if classified."""
    if not movie.genres:
        # mark unclassified? We'll leave genre_links empty; caller can check
        return False
    # Build lookup
    genres_by_tmdb = {g.tmdb_id: g for g in db.query(Genre).all() if g.tmdb_id is not None}
    genres_by_name = {g.name.lower(): g for g in db.query(Genre).all()}
    assigned = set()
    for g in movie.genres:
        genre_obj = None
        if isinstance(g, int):
            genre_obj = genres_by_tmdb.get(g)
        elif isinstance(g, str):
            # could be id string or name
            if g.isdigit():
                genre_obj = genres_by_tmdb.get(int(g))
            else:
                genre_obj = genres_by_name.get(g.lower())
                # also try TMDB map
                if genre_obj is None:
                    # maybe name not in map; skip
                    pass
        if genre_obj and genre_obj.id not in assigned:
            if genre_obj not in movie.genre_links:
                movie.genre_links.append(genre_obj)
            assigned.add(genre_obj.id)
    db.commit()
    return len(assigned) > 0


def classify_all(db: Session) -> dict:
    ensure_genres_from_tmdb(db)
    movies = db.query(Movie).all()
    classified = 0
    unclassified = 0
    errors = []
    for m in movies:
        try:
            ok = classify_movie(db, m)
            if ok:
                classified += 1
            else:
                unclassified += 1
        except Exception as e:
            errors.append(f"{m.id}: {e}")
    return {"total": len(movies), "classified": classified, "unclassified": unclassified, "errors": errors}
