"""User library (liked songs) management."""

from spotify.auth import get_spotify_client
from spotify.player import get_current_track


def _sp():
    """Lazy client so import never needs credentials."""
    return get_spotify_client()


def _current_track_id() -> tuple:
    """Return (track_id, track_dict) or raise with a clear message."""
    current_track = get_current_track()
    if current_track is None:
        raise Exception("No track currently playing")
    track_id = current_track.get("id")
    if track_id is None:
        raise Exception("Current track has no valid ID")
    return track_id, current_track


def like_current_song():
    """
    Add current playing track
    to user's liked songs.
    """
    track_id, current_track = _current_track_id()
    _sp().current_user_saved_tracks_add([track_id])
    return {
        "success": True,
        "track_name": current_track.get("name"),
        "artist": current_track.get("artist"),
    }


def unlike_current_song():
    """
    Remove current playing track
    from user's liked songs.
    """
    track_id, current_track = _current_track_id()
    _sp().current_user_saved_tracks_delete([track_id])
    return {
        "success": True,
        "track_name": current_track.get("name"),
        "artist": current_track.get("artist"),
    }


def is_current_song_liked():
    """
    Check if current track
    is already liked.
    """
    try:
        track_id, _ = _current_track_id()
    except Exception:
        return False
    result = _sp().current_user_saved_tracks_contains([track_id])
    if not result:
        return False
    return bool(result[0])
