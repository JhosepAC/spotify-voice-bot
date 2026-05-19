from spotify.search import (
    search_track,
    search_artist,
    search_album,
    search_playlist
)

from semantic.fuzzy_matcher import (
    find_best_match
)



def resolve_track(track_name):
    """
    Resolve Spotify track.
    """

    results = search_track(track_name)

    if not results:
        return track_name

    candidates = [
        track["name"]
        for track in results
    ]

    best_match = find_best_match(
        track_name,
        candidates
    )

    if best_match:
        return best_match

    return candidates[0]



def resolve_artist(artist_name):
    """
    Resolve Spotify artist.
    """

    results = search_artist(artist_name)

    if not results:
        return artist_name

    candidates = [
        artist["name"]
        for artist in results
    ]

    best_match = find_best_match(
        artist_name,
        candidates
    )

    if best_match:
        return best_match

    return candidates[0]