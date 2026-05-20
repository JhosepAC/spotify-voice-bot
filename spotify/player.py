from spotify.auth import (
    get_spotify_client
)

from spotify.device import (
    validate_active_device
)

from spotify.search import (
    search_track
)


sp = get_spotify_client()


def play_track(
    track_name
):
    """
    Search and play Spotify track.
    """

    validate_active_device()

    results = search_track(
        track_name,
        limit=1
    )

    if not results:

        raise Exception(
            "Track not found"
        )

    track = results[0]

    track_uri = track.get(
        "uri"
    )

    if not track_uri:

        raise Exception(
            "Invalid track URI"
        )

    sp.start_playback(
        uris=[track_uri]
    )


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


def set_volume(
    volume_percent
):
    """
    Set Spotify playback volume.
    """

    validate_active_device()

    volume_percent = max(
        0,
        min(100, volume_percent)
    )

    sp.volume(volume_percent)


def get_current_track():
    """
    Get current Spotify track.
    """

    validate_active_device()

    current_playback = (
        sp.current_playback()
    )

    if current_playback is None:

        return None

    track = current_playback.get(
        "item"
    )

    if track is None:

        return None

    artists = track.get(
        "artists",
        []
    )

    artist_name = "Unknown"

    if artists:

        artist_name = artists[0].get(
            "name",
            "Unknown"
        )

    album = track.get(
        "album",
        {}
    )

    return {
        "id": track.get("id"),
        "name": track.get("name"),
        "artist": artist_name,
        "album": album.get(
            "name",
            "Unknown"
        ),
        "is_playing": current_playback.get(
            "is_playing",
            False
        )
    }