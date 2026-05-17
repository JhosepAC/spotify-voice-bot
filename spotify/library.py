from spotify.auth import get_spotify_client
from spotify.device import validate_active_device

sp = get_spotify_client()

# =========================
# Library management functions
# =========================
# These functions allow you to like or unlike the currently playing track, and check if it's liked or not.

# Helper function to get the current track ID
def _get_current_track_id():
    """
    Get current playing track ID.
    """

    validate_active_device()

    current_playback = sp.current_playback()

    if not current_playback:
        return None

    track = current_playback.get("item")

    if not track:
        return None

    return track.get("id")

# Helper function to get the current track name
def like_current_track():
    """
    Save current track to library.
    """

    track_id = _get_current_track_id()

    if not track_id:
        return False

    sp.current_user_saved_tracks_add(
        [track_id]
    )

    return True

# Helper function to check if the current track is liked
def is_current_track_liked():
    """
    Check if current track is liked.
    """

    track_id = _get_current_track_id()

    if not track_id:
        return False

    results = sp.current_user_saved_tracks_contains(
        [track_id]
    )

    return results[0]

# Helper function to remove the current track from the library
def remove_like_current_track():
    """
    Remove current track from library.
    """

    track_id = _get_current_track_id()

    if not track_id:
        return False

    sp.current_user_saved_tracks_delete(
        [track_id]
    )

    return True