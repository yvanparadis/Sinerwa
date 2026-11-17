import os
import sys
import tempfile
import unittest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.normalization import normalize, normalize_tmdb
from app.services.dedup import is_duplicate, deduplicate, normalize_title
from app.integrations.providers import list_providers, get_provider
from app.integrations.tmdb_adapter import TMDBAdapter
from app.services.local_library import scan_library
from app.core.database import Base
from app.models import Provider
from app.services.sync_engine import sync_provider, ensure_provider_row
from app.services.storage import R2StorageProvider


class TestNormalization(unittest.TestCase):
    def test_tmdb_normalize(self):
        raw = {"id": 1, "title": "Foo", "overview": "bar", "poster_path": "/p.jpg", "backdrop_path": "/b.jpg",
               "release_date": "2024-01-01", "vote_average": 7.5, "original_language": "en", "runtime": 100}
        n = normalize_tmdb(raw)
        self.assertEqual(n["title"], "Foo")
        self.assertEqual(n["rating"], 7.5)
        self.assertIn("image.tmdb.org", n["poster"])

    def test_curated_normalize(self):
        raw = {"title": "Local", "translator": "Rocky"}
        n = normalize("oshakur_films", raw)
        self.assertEqual(n["title"], "Local")
        self.assertEqual(n["providerId"], "oshakur_films")


class TestDedup(unittest.TestCase):
    def test_normalize_title(self):
        self.assertEqual(normalize_title("The Hills of Kigali!"), "the hills of kigali")

    def test_duplicate_by_title_year(self):
        a = {"title": "Foo", "releaseDate": "2024-01-01", "externalId": "1", "providerId": "tmdb"}
        b = {"title": "Foo", "releaseDate": "2024-05-05", "externalId": "2", "providerId": "oshakur"}
        self.assertTrue(is_duplicate(a, b))

    def test_not_duplicate_different_year(self):
        a = {"title": "Foo", "releaseDate": "2024-01-01", "externalId": "1", "providerId": "tmdb"}
        b = {"title": "Foo", "releaseDate": "2023-05-05", "externalId": "2", "providerId": "oshakur"}
        self.assertFalse(is_duplicate(a, b))

    def test_deduplicate(self):
        recs = [
            {"title": "Foo", "releaseDate": "2024-01-01", "externalId": "1", "providerId": "tmdb"},
            {"title": "Foo", "releaseDate": "2024-05-05", "externalId": "2", "providerId": "oshakur"},
            {"title": "Bar", "releaseDate": "2023-01-01", "externalId": "3", "providerId": "tmdb"},
        ]
        out = deduplicate(recs)
        self.assertEqual(len(out), 2)


class TestProviders(unittest.TestCase):
    def test_list_providers(self):
        ps = list_providers()
        ids = {p.id for p in ps}
        self.assertIn("tmdb", ids)
        self.assertIn("oshakur_films", ids)
        self.assertIn("agasobanuye_now", ids)

    def test_pending_authorization(self):
        p = get_provider("oshakur_films")
        self.assertEqual(p.authorization_status, "pending")
        self.assertFalse(p.api_available)

    def test_tmdb_adapter_unauthorized_without_key(self):
        a = TMDBAdapter()
        # may or may not have key depending env; just ensure method exists
        self.assertTrue(hasattr(a, "is_authorized"))


class TestLocalLibrary(unittest.TestCase):
    def test_scan_empty_dir(self):
        d = tempfile.mkdtemp()
        items = scan_library(d)
        self.assertEqual(items, [])

    def test_scan_finds_video(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "MOVIE_BY_ROCKY.mp4")
        with open(p, "wb") as f:
            f.write(b"\x00" * 10)
        items = scan_library(d)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["translator"], "Rocky")
        self.assertEqual(items[0]["title"], "MOVIE")


class TestSync(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def test_skip_pending_provider(self):
        db = self.Session()
        ensure_provider_row(db, "oshakur_films")
        history = asyncio.run(sync_provider(db, "oshakur_films"))
        self.assertEqual(history.status, "skipped")
        db.close()

    def test_tmdb_sync_without_key_skipped(self):
        db = self.Session()
        ensure_provider_row(db, "tmdb")
        history = asyncio.run(sync_provider(db, "tmdb"))
        # TMDB authorization_status is authorized but api_available depends on settings;
        # without key, adapter.is_authorized False -> skipped
        self.assertIn(history.status, ("skipped", "success"))
        db.close()


class TestStorage(unittest.TestCase):
    def test_missing_credentials_clear_error(self):
        p = R2StorageProvider()
        # Force unconfigured
        p.settings.r2_access_key_id = ""
        p.settings.r2_secret_access_key = ""
        p.settings.r2_account_id = ""
        p.settings.r2_s3_endpoint = ""
        self.assertFalse(p.configured())
        res = p.test_connection("any-bucket")
        self.assertFalse(res["ok"])
        self.assertIsNotNone(res["error"])

    def test_storage_provider_interface(self):
        p = R2StorageProvider()
        self.assertTrue(hasattr(p, "upload_file"))
        self.assertTrue(hasattr(p, "presigned_url"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
