"""User playlist management: list, create and extend playlists."""

from rapidfuzz import fuzz

from nlp.normalizer import normalize
from spotify.auth import get_spotify_client
from spotify.player import get_current_track


def _sp():
    """Lazy client so import never needs credentials."""
    return get_spotify_client()


def list_my_playlists(limit: int = 10) -> list[dict]:
    """Return the user's playlists as [{id, name, uri}]."""
    try:
        data = _sp().current_user_playlists(limit=limit) or {}
        return [
            {"id": p.get("id"), "name": p.get("name", ""), "uri": p.get("uri")}
            for p in data.get("items", [])
            if p.get("id")
        ]
    except Exception as e:
        print(f"[Playlists] list error: {e}")
        return []


def find_playlist(name: str) -> dict | None:
    """Fuzzy-find one of the user's playlists by name."""
    target = normalize(name)
    best, best_score = None, 0.0
    for playlist in list_my_playlists(limit=20):
        score = float(fuzz.token_set_ratio(target, normalize(playlist["name"])))
        if score > best_score:
            best_score, best = score, playlist
    return best if best is not None and best_score >= 60.0 else None


def create_playlist(name: str) -> dict:
    """Create a private playlist. Returns {success, label}."""
    try:
        user = _sp().current_user() or {}
        new = _sp().user_playlist_create(
            user.get("id"), name.strip(), public=False
        )
        return {"success": True, "label": new.get("name", name)}
    except Exception as e:
        print(f"[Playlists] create error: {e}")
        return {"success": False, "label": None}


def add_current_track_to_playlist(name: str) -> dict:
    """
    Add the now-playing track to a named playlist.

    Returns {success, track, playlist} or {success False, missing} when
    the playlist does not exist yet.
    """
    try:
        track = get_current_track()
        if not track or not track.get("id"):
            return {"success": False, "track": None, "playlist": None}
        playlist = find_playlist(name)
        if playlist is None:
            return {
                "success": False,
                "track": track.get("name"),
                "playlist": None,
                "missing": name,
            }
        _sp().playlist_add_items(playlist["id"], [track["id"]])
        return {
            "success": True,
            "track": track.get("name"),
            "playlist": playlist["name"],
        }
    except Exception as e:
        print(f"[Playlists] add error: {e}")
        return {"success": False, "track": None, "playlist": None}
