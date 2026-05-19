from semantic.spotify_matcher import (
    resolve_track
)


def correct_track_command(track_name):
    """
    Correct track name semantically.
    """

    resolved_track = resolve_track(
        track_name
    )

    return resolved_track