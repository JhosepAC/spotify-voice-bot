from spotify.auth import (
    get_spotify_client
)

from spotify.player import (
    get_current_track
)


sp = get_spotify_client()


def like_current_song():
    """
    Add current playing track
    to user's liked songs.
    """

    current_track = (
        get_current_track()
    )

    if current_track is None:

        raise Exception(
            "No track currently playing"
        )

    track_id = current_track.get(
        "id"
    )

    if track_id is None:

        raise Exception(
            "Current track has no valid ID"
        )

    sp.current_user_saved_tracks_add(
        [track_id]
    )

    return {
        "success": True,
        "track_name": current_track.get(
            "name"
        ),
        "artist": current_track.get(
            "artist"
        )
    }


def unlike_current_song():
    """
    Remove current playing track
    from user's liked songs.
    """

    current_track = (
        get_current_track()
    )

    if current_track is None:

        raise Exception(
            "No track currently playing"
        )

    track_id = current_track.get(
        "id"
    )

    if track_id is None:

        raise Exception(
            "Current track has no valid ID"
        )

    sp.current_user_saved_tracks_delete(
        [track_id]
    )

    return {
        "success": True,
        "track_name": current_track.get(
            "name"
        ),
        "artist": current_track.get(
            "artist"
        )
    }


def is_current_song_liked():
    """
    Check if current track
    is already liked.
    """

    current_track = (
        get_current_track()
    )

    if current_track is None:

        return False

    track_id = current_track.get(
        "id"
    )

    if track_id is None:

        return False

    result = (
        sp.current_user_saved_tracks_contains(
            [track_id]
        )
    )

    if not result:

        return False

    return bool(result[0])