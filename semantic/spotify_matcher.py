from spotify.search import (
    search_tracks,
    search_artist
)

from semantic.fuzzy_matcher import (
    find_best_match
)


SEARCH_LIMIT = 10


def resolve_track_name(
    query
):
    """
    Resolve real Spotify track.
    """

    results = search_tracks(

        query,

        limit=SEARCH_LIMIT
    )

    if not results:

        return None

    candidate_names = [

        track["name"]

        for track in results
    ]

    return find_best_match(

        query,

        candidate_names
    )


def resolve_artist_name(
    query
):
    """
    Resolve real Spotify artist.
    """

    results = search_artist(

        query,

        limit=SEARCH_LIMIT
    )

    if not results:

        return None

    candidate_names = [

        artist["name"]

        for artist in results
    ]

    return find_best_match(

        query,

        candidate_names
    )