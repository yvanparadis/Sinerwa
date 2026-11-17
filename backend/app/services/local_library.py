import os
import re
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

VIDEO_EXTS = {".mp4", ".avi", ".mpg", ".mpeg", ".ts", ".wmv", ".mkv"}
SUBTITLE_EXTS = {".srt", ".vtt"}

DEFAULT_ROOT = os.environ.get("LOCAL_MOVIES_DIR", "F:/Paradis/movies")


def _safe_root() -> Path:
    return Path(DEFAULT_ROOT).resolve()


def _is_video(p: Path) -> bool:
    return p.suffix.lower() in VIDEO_EXTS


def _clean_title(name: str) -> str:
    # Strip extension
    stem = Path(name).stem
    # Remove translator suffixes and quality tags
    s = stem
    s = re.sub(r"AGASOBANUYE.*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"BY_[A-Z ]+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\(\d+p\)", "", s)
    s = s.replace("_", " ").replace("~", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # Remove trailing part letters like " A", " B" keep but okay
    return s or stem


def _detect_translator(name: str) -> Optional[str]:
    m = re.search(r"BY[_ ]+([A-Za-z ]+?)(?:AGASOBANUYE|_|\(|$)", name, re.IGNORECASE)
    if m:
        cand = m.group(1).strip().replace("_", " ")
        if cand:
            return cand.title()
    # common pattern: "BY ROCKY"
    m2 = re.search(r"BY[_ ]+([A-Za-z]+)", name, re.IGNORECASE)
    if m2:
        return m2.group(1).title()
    return None


def _detect_series(title: str) -> Optional[str]:
    # patterns like S02E2, S2 EP1, EP_07, E01
    m = re.search(r"S(\d+)", title, re.IGNORECASE)
    if m:
        return f"Season {int(m.group(1))}"
    return None


def _detect_episode(title: str) -> Optional[str]:
    m = re.search(r"E(?:P)?[_ ]?(\d+)", title, re.IGNORECASE)
    if m:
        return f"Episode {int(m.group(1))}"
    m2 = re.search(r"EP[_ ]?(\d+)", title, re.IGNORECASE)
    if m2:
        return f"Episode {int(m2.group(1))}"
    return None


def scan_library(root: Optional[str] = None) -> List[Dict[str, Any]]:
    base = Path(root).resolve() if root else _safe_root()
    if not base.exists():
        return []
    items: List[Dict[str, Any]] = []
    idx = 0
    for p in sorted(base.rglob("*")):
        if not p.is_file() or not _is_video(p):
            continue
        rel = p.relative_to(base).as_posix()
        title = _clean_title(p.name)
        # subtitle lookup
        sub = None
        for ext in SUBTITLE_EXTS:
            cand = p.with_suffix(ext)
            if cand.exists():
                sub = cand.relative_to(base).as_posix()
                break
            # also same stem .srt in same dir
        # find any srt with same stem prefix
        if sub is None:
            for s in p.parent.glob(p.stem + ".*"):
                if s.suffix.lower() in SUBTITLE_EXTS:
                    sub = s.relative_to(base).as_posix()
                    break

        translator = _detect_translator(p.name)
        season = _detect_series(p.name)
        episode = _detect_episode(p.name)

        content_type = "movie"
        if season or episode or "EP" in p.name.upper() or re.search(r"S\d+E\d+", p.name, re.IGNORECASE):
            content_type = "episode"

        items.append({
            "id": f"local-{idx}",
            "title": title,
            "path": rel,
            "url": "/api/v1/local/media/" + urllib.parse.quote(rel, safe=""),
            "subtitleUrl": ("/api/v1/local/media/" + urllib.parse.quote(sub, safe="")) if sub else None,
            "translator": translator,
            "contentType": content_type,
            "season": season,
            "episode": episode,
            "size": p.stat().st_size,
            "extension": p.suffix.lower(),
        })
        idx += 1
    return items
