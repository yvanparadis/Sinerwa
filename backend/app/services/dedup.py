import re
from typing import List, Dict, Any, Optional


def normalize_title(title: Optional[str]) -> str:
    if not title:
        return ""
    t = title.lower().strip()
    t = re.sub(r"[^a-z0-9\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


def release_year(release_date: Optional[str]) -> Optional[str]:
    if not release_date:
        return None
    return str(release_date)[:4]


def is_duplicate(candidate: Dict[str, Any], existing: Dict[str, Any]) -> bool:
    # External id match within same provider
    if candidate.get("externalId") and candidate.get("externalId") == existing.get("externalId") \
            and candidate.get("providerId") == existing.get("providerId"):
        return True
    # Cross-provider: normalized title + year
    if normalize_title(candidate.get("title")) == normalize_title(existing.get("title")) \
            and release_year(candidate.get("releaseDate")) == release_year(existing.get("releaseDate")) \
            and release_year(candidate.get("releaseDate")) is not None:
        return True
    return False


def find_duplicates(candidate: Dict[str, Any], catalog: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [m for m in catalog if is_duplicate(candidate, m)]


def deduplicate(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for r in records:
        if any(is_duplicate(r, e) for e in result):
            continue
        result.append(r)
    return result
