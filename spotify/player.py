from spotify.auth import get_spotify_client
from spotify.device import validate_active_device

sp = get_spotify_client()


def pause_playback():
    """
    Pause current Spotify playback.
    """

    validate_active_device()

    sp.pause_playback()


def resume_playback():
    """
    Resume Spotify playback.
    """

    validate_active_device()

    sp.start_playback()


def next_track():
    """
    Skip to next track.
    """

    validate_active_device()

    sp.next_track()


def previous_track():
    """
    Return to previous track.
    """

    validate_active_device()

    sp.previous_track()


def set_volume(volume_percent):
    """
    Set Spotify playback volume.

    Args:
        volume_percent (int): value between 0 and 100
    """

    validate_active_device()

    volume_percent = max(0, min(100, volume_percent))

    sp.volume(volume_percent)


def get_current_track():
    """
    Get current playing track information.

    Returns:
        dict | None
    """

    validate_active_device()

    current_playback = sp.current_playback()

    if not current_playback:
        return None

    track = current_playback.get("item")

    if not track:
        return None

    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "is_playing": current_playback["is_playing"]
    }