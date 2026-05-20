from semantic.spotify_matcher import (
    resolve_track_name,
    resolve_artist_name
)


def correct_track_command(
    track_name
):
    """
    Correct Spotify track name.
    """

    result = resolve_track_name(
        track_name
    )

    if result is None:

        return None

    return result.get(
        "name"
    )


def correct_artist_command(
    artist_name
):
    """
    Correct Spotify artist name.
    """

    result = resolve_artist_name(
        artist_name
    )

    if result is None:

        return None

    return result.get(
        "name"
    )