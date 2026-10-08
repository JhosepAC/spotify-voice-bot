"""
Spotify playback control.
Handles tracks, artists, albums, playlists, volume.
"""

from typing import Any

from spotify.auth import get_spotify_client
from spotify.device import validate_active_device
from spotify.search import pick_best, display_label


def _sp():
    """Lazy client so importing this module never crashes without credentials."""
    return get_spotify_client()


def _get_device_id() -> str | None:
    try:
        device = validate_active_device()
        return device.get("id")
    except Exception:
        return None


def resolve_and_play(query: str, search_type: str = "track") -> dict:
    """
    Search top candidates, fuzzy-pick the best one, and play it.

    Returns:
        {"success": bool, "label": str | None, "score": float,
         "candidates": [{"uri": str, "label": str}]}
        Label is the API-verified name to speak back to the user.
    """
    try:
        client = _sp()
        device_id = _get_device_id()

        results = client.search(q=query, type=search_type, limit=5)
        if results is None:
            return {"success": False, "label": None, "score": 0.0, "candidates": []}

        items = results.get(f"{search_type}s", {}).get("items", [])
        if not items:
            return {"success": False, "label": None, "score": 0.0, "candidates": []}

        best, score = pick_best(query, items, search_type)
        if best is None or score < 45.0:
            best = items[0]

        uri = best.get("uri")
        if not uri:
            return {"success": False, "label": None, "score": score, "candidates": []}

        if search_type == "track":
            client.start_playback(device_id=device_id, uris=[uri])
        else:
            client.start_playback(device_id=device_id, context_uri=uri)

        candidates = [
            {"uri": it.get("uri"), "label": display_label(it, search_type)}
            for it in items[:5]
            if it.get("uri")
        ]
        return {
            "success": True,
            "label": display_label(best, search_type),
            "score": score,
            "candidates": candidates,
        }
    except Exception as e:
        print(f"[Player] resolve_and_play error: {e}")
        return {"success": False, "label": None, "score": 0.0, "candidates": []}


def play_track(query: str, search_type: str = "track") -> bool:
    """
    Search and play a track, album, or playlist by query string.
    Returns True on success.
    """
    return bool(resolve_and_play(query, search_type).get("success"))


def resolve_artist(artist_name: str) -> dict:
    """Fuzzy-pick the best artist and play their top tracks."""
    try:
        client = _sp()
        device_id = _get_device_id()
        results = client.search(q=artist_name, type="artist", limit=5)
        if results is None:
            return {"success": False, "label": None, "score": 0.0}
        artists = results.get("artists", {}).get("items", [])
        if not artists:
            return {"success": False, "label": None, "score": 0.0}
        best, score = pick_best(artist_name, artists, "artist")
        if best is None:
            return {"success": False, "label": None, "score": 0.0}
        uri = best.get("uri")
        if not uri:
            return {"success": False, "label": None, "score": 0.0}
        client.start_playback(device_id=device_id, context_uri=uri)
        return {"success": True, "label": best.get("name"), "score": score}
    except Exception as e:
        print(f"[Player] resolve_artist error: {e}")
        return {"success": False, "label": None, "score": 0.0}


def play_artist(artist_name: str) -> bool:
    """
    Find artist and play their top tracks.
    """
    return bool(resolve_artist(artist_name).get("success"))


def play_candidate(uri: str, search_type: str = "track") -> bool:
    """Play an already-resolved Spotify URI (disambiguation picks)."""
    try:
        client = _sp()
        device_id = _get_device_id()
        if search_type == "track":
            client.start_playback(device_id=device_id, uris=[uri])
        else:
            client.start_playback(device_id=device_id, context_uri=uri)
        return True
    except Exception as e:
        print(f"[Player] play_candidate error: {e}")
        return False


def pause_playback():
    try:
        _sp().pause_playback(device_id=_get_device_id())
    except Exception as e:
        print(f"[Player] pause error: {e}")


def resume_playback():
    try:
        _sp().start_playback(device_id=_get_device_id())
    except Exception as e:
        print(f"[Player] resume error: {e}")


def next_track():
    try:
        _sp().next_track(device_id=_get_device_id())
    except Exception as e:
        print(f"[Player] next_track error: {e}")


def previous_track():
    try:
        _sp().previous_track(device_id=_get_device_id())
    except Exception as e:
        print(f"[Player] previous_track error: {e}")


def set_volume(volume_percent: int):
    try:
        volume_percent = max(0, min(100, volume_percent))
        _sp().volume(volume_percent, device_id=_get_device_id())
    except Exception as e:
        print(f"[Player] set_volume error: {e}")


def get_current_volume() -> int:
    """
    Returns current playback volume (0-100). Defaults to 50.
    """
    try:
        playback = _sp().current_playback()
        if playback and playback.get("device"):
            return playback["device"].get("volume_percent", 50)
        return 50
    except Exception:
        return 50


def get_current_track() -> dict[str, Any] | None:
    """
    Returns info about the currently playing track.
    """
    try:
        playback = _sp().current_playback()
        if not playback:
            return None

        track = playback.get("item")
        if not track:
            return None

        artists = track.get("artists", [])
        artist_name = artists[0].get("name", "Unknown") if artists else "Unknown"

        return {
            "id": track.get("id"),
            "name": track.get("name"),
            "artist": artist_name,
            "album": track.get("album", {}).get("name", "Unknown"),
            "is_playing": playback.get("is_playing", False),
        }

    except Exception as e:
        print(f"[Player] get_current_track error: {e}")
        return None
