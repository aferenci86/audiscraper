"""Listing filter logic. Every scraper normalizes to a dict, then runs through `matches()`."""
import re
from config import (
    MAX_MILES, REQUIRED_KEYWORDS_ANY, REQUIRE_MANUAL_TRANSMISSION,
    ALLOWED_ENGINES, AUTO_TRANS_NEGATIVES, MANUAL_POSITIVES,
)


def _norm(s: str) -> str:
    return (s or "").lower()


def extract_miles(text: str):
    """Pull a mileage number out of freeform text. Returns int or None."""
    if not text:
        return None
    t = text.lower().replace(",", "")
    # Patterns like "42k miles", "42,000 miles", "42000 mi"
    patterns = [
        r"(\d{1,3})\s*k\s*(?:mi|miles|mile)\b",           # "42k miles"
        r"(\d{3,6})\s*(?:mi|miles|mile)\b",               # "42000 miles"
        r"odometer[:\s]+(\d{3,6})",                       # "odometer: 42000"
        r"mileage[:\s]+(\d{1,3})\s*k\b",                  # "mileage: 42k"
        r"mileage[:\s]+(\d{3,6})",                        # "mileage: 42000"
    ]
    for i, pat in enumerate(patterns):
        m = re.search(pat, t)
        if m:
            n = int(m.group(1))
            # The "k" patterns
            if i in (0, 3):
                return n * 1000
            return n
    return None


def looks_like_manual(text: str) -> bool:
    t = _norm(text)
    if any(neg in t for neg in AUTO_TRANS_NEGATIVES):
        # Explicit auto-transmission markers — reject unless also says "manual"
        if not any(pos in t for pos in MANUAL_POSITIVES):
            return False
    return any(pos in t for pos in MANUAL_POSITIVES) or "manual" in t


def engine_match(text: str) -> bool:
    t = _norm(text)
    # Accept "v8", "v-8", "4.2", "v10", "v-10", "5.2"
    engine_hints = {
        "v8": ["v8", "v-8", "4.2l", "4.2 l", " 4.2 "],
        "v10": ["v10", "v-10", "5.2l", "5.2 l", " 5.2 "],
    }
    for eng in ALLOWED_ENGINES:
        if any(h in t for h in engine_hints.get(eng, [])):
            return True
    return False


def matches(listing: dict) -> bool:
    """Core filter. `listing` needs `title`, `description` (optional), `miles` (optional int)."""
    blob = " ".join([
        listing.get("title", ""),
        listing.get("description", ""),
        listing.get("subtitle", ""),
    ])
    t = _norm(blob)

    # Must be an R8
    if not any(k in t for k in REQUIRED_KEYWORDS_ANY):
        return False

    # Engine: V8 or V10
    if not engine_match(blob):
        return False

    # Transmission: manual
    if REQUIRE_MANUAL_TRANSMISSION and not looks_like_manual(blob):
        return False

    # Mileage
    miles = listing.get("miles")
    if miles is None:
        miles = extract_miles(blob)
    if miles is None:
        # Unknown mileage — keep it; better to surface than miss. SMS will note "mi: ?"
        listing["miles"] = None
        return True
    listing["miles"] = miles
    return miles <= MAX_MILES
