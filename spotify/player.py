"""
Spotify playback control.
Handles tracks, artists, albums, playlists, volume.
"""

from spotify.auth import get_spotify_client
from spotify.device import validate_active_device
from typing import Any

sp = get_spotify_client()


def _get_device_id() -> str | None:
    try:
        device = validate_active_device()
        return device.get("id")
    except Exception:
        return None


def play_track(query: str, search_type: str = "track") -> bool:
    """
    Search and play a track, album, or playlist by query string.
    Returns True on success.
    """
    try:
        device_id = _get_device_id()

        results = sp.search(q=query, type=search_type, limit=1)

        if results is None:
            return False

        items_key = f"{search_type}s"
        items = results.get(items_key, {}).get("items", [])

        if not items:
            return False

        item = items[0]
        uri = item.get("uri")

        if not uri:
            return False

        if search_type == "track":
            sp.start_playback(device_id=device_id, uris=[uri])
        else:
            sp.start_playback(device_id=device_id, context_uri=uri)

        return True

    except Exception as e:
        print(f"[Player] play_track error: {e}")
        return False


def play_artist(artist_name: str) -> bool:
    """
    Find artist and play their top tracks.
    """
    try:
        device_id = _get_device_id()

        results = sp.search(q=artist_name, type="artist", limit=1)

        if results is None:
            return False

        artists = results.get("artists", {}).get("items", [])

        if not artists:
            return False

        artist_uri = artists[0].get("uri")

        if not artist_uri:
            return False

        sp.start_playback(device_id=device_id, context_uri=artist_uri)

        return True

    except Exception as e:
        print(f"[Player] play_artist error: {e}")
        return False

def pause_playback():
    try:
        device_id = _get_device_id()
        sp.pause_playback(device_id=device_id)
    except Exception as e:
        print(f"[Player] pause error: {e}")


def resume_playback():
    try:
        device_id = _get_device_id()
        sp.start_playback(device_id=device_id)
    except Exception as e:
        print(f"[Player] resume error: {e}")


def next_track():
    try:
        device_id = _get_device_id()
        sp.next_track(device_id=device_id)
    except Exception as e:
        print(f"[Player] next_track error: {e}")


def previous_track():
    try:
        device_id = _get_device_id()
        sp.previous_track(device_id=device_id)
    except Exception as e:
        print(f"[Player] previous_track error: {e}")


def set_volume(volume_percent: int):
    try:
        device_id = _get_device_id()
        volume_percent = max(0, min(100, volume_percent))
        sp.volume(volume_percent, device_id=device_id)
    except Exception as e:
        print(f"[Player] set_volume error: {e}")


def get_current_volume() -> int:
    """
    Returns current playback volume (0–100). Defaults to 50.
    """
    try:
        playback = sp.current_playback()
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
        playback = sp.current_playback()
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
