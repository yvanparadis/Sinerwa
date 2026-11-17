from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import Movie, Genre
from datetime import datetime

BASE = "https://cinerwa.vercel.app"

STATIC_PAGES = [
    ("/", "1.0", "daily"),
    ("/movies", "0.9", "daily"),
    ("/series", "0.8", "weekly"),
    ("/about", "0.5", "monthly"),
    ("/search", "0.6", "weekly"),
]


def generate_sitemap() -> str:
    db = SessionLocal()
    try:
        urls = []
        for path, prio, freq in STATIC_PAGES:
            urls.append((f"{BASE}{path}", datetime.utcnow().date().isoformat(), freq, prio))

        for m in db.query(Movie).all():
            lastmod = m.updated_at.isoformat() if m.updated_at else datetime.utcnow().date().isoformat()
            urls.append((f"{BASE}/movie/{m.id}", lastmod[:10], "weekly", "0.8"))

        for g in db.query(Genre).all():
            urls.append((f"{BASE}/movies?genre={g.slug}", datetime.utcnow().date().isoformat(), "weekly", "0.7"))

        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for loc, lastmod, freq, prio in urls:
            xml.append("  <url>")
            xml.append(f"    <loc>{loc}</loc>")
            xml.append(f"    <lastmod>{lastmod}</lastmod>")
            xml.append(f"    <changefreq>{freq}</changefreq>")
            xml.append(f"    <priority>{prio}</priority>")
            xml.append("  </url>")
        xml.append("</urlset>")
        return "\n".join(xml)
    finally:
        db.close()
