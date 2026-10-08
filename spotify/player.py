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


def _search_best(query: str, search_type: str = "track") -> tuple:
    """
    Search top candidates and fuzzy-pick the best one (no playback).

    Returns (items, best_item_or_None, score).
    """
    client = _sp()
    results = client.search(q=query, type=search_type, limit=5)
    if results is None:
        return [], None, 0.0
    items = results.get(f"{search_type}s", {}).get("items", [])
    if not items:
        return [], None, 0.0
    best, score = pick_best(query, items, search_type)
    if best is None or score < 45.0:
        best = items[0]
    return items, best, score


def preview_candidates(query: str, search_type: str = "track") -> dict:
    """
    Search without playing, for low-confidence confirmations.

    Returns {"label", "score", "candidates": [{uri, label, search_type}]}.
    """
    try:
        items, best, score = _search_best(query, search_type)
        if best is None:
            return {"label": None, "score": 0.0, "candidates": []}
        candidates = [
            {
                "uri": it.get("uri"),
                "label": display_label(it, search_type),
                "search_type": search_type,
            }
            for it in items[:5]
            if it.get("uri")
        ]
        return {"label": display_label(best, search_type), "score": score, "candidates": candidates}
    except Exception as e:
        print(f"[Player] preview error: {e}")
        return {"label": None, "score": 0.0, "candidates": []}


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

        items, best, score = _search_best(query, search_type)
        if best is None:
            return {"success": False, "label": None, "score": 0.0, "candidates": []}

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


def get_playback_state() -> dict | None:
    """Return raw current playback dict (or None when idle)."""
    try:
        return _sp().current_playback()
    except Exception as e:
        print(f"[Player] playback state error: {e}")
        return None


def seek_forward(seconds: int = 30) -> int:
    """Jump forward; returns the new position in seconds."""
    try:
        playback = get_playback_state() or {}
        pos = int(playback.get("progress_ms") or 0)
        new_pos = pos + max(1, seconds) * 1000
        _sp().seek_track(new_pos, device_id=_get_device_id())
        return new_pos // 1000
    except Exception as e:
        print(f"[Player] seek_forward error: {e}")
        return -1


def seek_back(seconds: int = 15) -> int:
    """Jump backward; returns the new position in seconds."""
    try:
        playback = get_playback_state() or {}
        pos = int(playback.get("progress_ms") or 0)
        new_pos = max(0, pos - max(1, seconds) * 1000)
        _sp().seek_track(new_pos, device_id=_get_device_id())
        return new_pos // 1000
    except Exception as e:
        print(f"[Player] seek_back error: {e}")
        return -1


def restart_track() -> bool:
    """Restart the current track from the beginning."""
    try:
        _sp().seek_track(0, device_id=_get_device_id())
        return True
    except Exception as e:
        print(f"[Player] restart error: {e}")
        return False


def toggle_playback() -> str:
    """Toggle play/pause. Returns 'playing', 'paused' or 'unknown'."""
    try:
        playback = get_playback_state()
        if not playback:
            return "unknown"
        if playback.get("is_playing"):
            pause_playback()
            return "paused"
        resume_playback()
        return "playing"
    except Exception as e:
        print(f"[Player] toggle error: {e}")
        return "unknown"


def skip_n(count: int) -> int:
    """Skip forward N tracks. Returns tracks actually skipped."""
    done = 0
    try:
        for _ in range(max(1, min(20, int(count)))):
            next_track()
            done += 1
    except Exception as e:
        print(f"[Player] skip_n error: {e}")
    return done


def set_shuffle(state: bool) -> bool:
    """Enable or disable shuffle. Returns True on success."""
    try:
        _sp().shuffle(bool(state), device_id=_get_device_id())
        return True
    except Exception as e:
        print(f"[Player] shuffle error: {e}")
        return False


def toggle_shuffle() -> bool | None:
    """Flip shuffle state. Returns the new state (or None on error)."""
    try:
        playback = get_playback_state() or {}
        new_state = not bool(playback.get("shuffle_state", False))
        if not set_shuffle(new_state):
            return None
        return new_state
    except Exception as e:
        print(f"[Player] toggle_shuffle error: {e}")
        return None


def set_repeat_mode(mode: str) -> bool:
    """Set repeat mode: 'track', 'context' or 'off'."""
    mode = mode if mode in ("track", "context", "off") else "track"
    try:
        _sp().repeat(mode, device_id=_get_device_id())
        return True
    except Exception as e:
        print(f"[Player] repeat error: {e}")
        return False


def queue_track(query: str) -> dict:
    """Resolve a track and add it to the queue (no playback change)."""
    try:
        items, best, score = _search_best(query, "track")
        if best is None or not best.get("uri"):
            return {"success": False, "label": None, "score": score}
        _sp().add_to_queue(best["uri"], device_id=_get_device_id())
        artists = best.get("artists", []) or []
        artist = artists[0].get("name", "") if artists else ""
        name = best.get("name", "")
        label = f"{name} de {artist}" if artist else name
        return {"success": True, "label": label, "score": score}
    except Exception as e:
        print(f"[Player] queue_track error: {e}")
        return {"success": False, "label": None, "score": 0.0}


def get_queue_labels(count: int = 3) -> list[str]:
    """Return the next few queued track labels."""
    try:
        data = _sp().queue() or {}
        labels = []
        for item in (data.get("queue", []) or [])[: max(1, count)]:
            artists = item.get("artists", []) or []
            artist = artists[0].get("name", "") if artists else ""
            name = item.get("name", "")
            labels.append(f"{name} de {artist}" if artist else name)
        return labels
    except Exception as e:
        print(f"[Player] queue list error: {e}")
        return []


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
