from semantic.spotify_matcher import (
    resolve_track_name,
    resolve_artist_name
)


def correct_track_command(
    track_name
):
    """
    Semantic track correction.
    """

    if not track_name:

        return None

    resolved_track = (
        resolve_track_name(
            track_name
        )
    )

    return resolved_track


def correct_artist_command(
    artist_name
):
    """
    Semantic artist correction.
    """

    if not artist_name:

        return None

    resolved_artist = (
        resolve_artist_name(
            artist_name
        )
    )

    return resolved_artist