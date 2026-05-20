from spotify.search import (
    search_track,
    search_artist
)

from semantic.fuzzy_matcher import (
    find_best_match
)


def resolve_track_name(
    query
):
    """
    Resolve best Spotify track.
    """

    candidates = search_track(
        query,
        limit=10
    )

    best_match = find_best_match(

        query,

        candidates
    )

    return best_match


def resolve_artist_name(
    query
):
    """
    Resolve best Spotify artist.
    """

    candidates = search_artist(
        query,
        limit=10
    )

    best_match = find_best_match(

        query,

        candidates
    )

    return best_match