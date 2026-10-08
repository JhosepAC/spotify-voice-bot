"""Fuzzy Spotify search: pick the best candidate, not the first one.

Compares the user query against top candidates with RapidFuzz
so STT noise ("blain dilait") still resolves to the right item.
"""

from rapidfuzz import fuzz

from nlp.normalizer import normalize


def item_label(item: dict, search_type: str) -> str:
    """Build a comparable label for a Spotify search item."""
    if search_type == "track":
        artists = item.get("artists", []) or []
        artist = artists[0].get("name", "") if artists else ""
        return f"{item.get('name', '')} {artist}".strip()
    if search_type == "artist":
        return str(item.get("name", ""))
    if search_type == "album":
        artists = item.get("artists", []) or []
        artist = artists[0].get("name", "") if artists else ""
        return f"{item.get('name', '')} {artist}".strip()
    if search_type == "playlist":
        return str(item.get("name", ""))
    return str(item.get("name", ""))


def pick_best(query: str, items: list, search_type: str = "track") -> tuple:
    """Return (best_item, score 0-100) using fuzzy matching."""
    norm_query = normalize(query)
    best = None
    best_score = 0.0
    for item in items:
        score = float(fuzz.token_set_ratio(norm_query, normalize(item_label(item, search_type))))
        if score > best_score:
            best_score = score
            best = item
    return best, best_score


def display_label(item: dict, search_type: str) -> str:
    """Human-friendly label verified by the API (speak this, not the query)."""
    if search_type == "track":
        artists = item.get("artists", []) or []
        artist = artists[0].get("name", "") if artists else ""
        name = item.get("name", "")
        return f"{name} de {artist}" if artist else name
    return str(item.get("name", ""))
