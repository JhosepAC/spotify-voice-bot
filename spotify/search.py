from spotify.auth import (
    get_spotify_client
)


sp = get_spotify_client()


SEARCH_LIMIT = 10


def safe_search(query, search_type, limit):
    """
    Safe Spotify search wrapper.
    """

    try:

        results = sp.search(
            q=query,
            type=search_type,
            limit=limit
        )

        if not results:
            return {}

        return results

    except Exception as error:

        print(
            f"Spotify Search Error: {error}"
        )

        return {}


def search_track(query, limit=SEARCH_LIMIT):
    """
    Search Spotify tracks.
    """

    results = safe_search(
        query,
        "track",
        limit
    )

    tracks = (
        results.get(
            "tracks",
            {}
        ).get(
            "items",
            []
        )
    )

    return [
        {
            "id": track.get("id"),

            "name": track.get("name"),

            "artist": (
                track.get(
                    "artists",
                    [{}]
                )[0].get("name")
            ),

            "album": (
                track.get(
                    "album",
                    {}
                ).get("name")
            ),

            "uri": track.get("uri")
        }

        for track in tracks
    ]


def search_artist(query, limit=SEARCH_LIMIT):
    """
    Search Spotify artists.
    """

    results = safe_search(
        query,
        "artist",
        limit
    )

    artists = (
        results.get(
            "artists",
            {}
        ).get(
            "items",
            []
        )
    )

    return [
        {
            "id": artist.get("id"),

            "name": artist.get("name"),

            "genres": artist.get(
                "genres",
                []
            ),

            "followers": (
                artist.get(
                    "followers",
                    {}
                ).get(
                    "total",
                    0
                )
            ),

            "uri": artist.get("uri")
        }

        for artist in artists
    ]


def search_album(query, limit=SEARCH_LIMIT):
    """
    Search Spotify albums.
    """

    results = safe_search(
        query,
        "album",
        limit
    )

    albums = (
        results.get(
            "albums",
            {}
        ).get(
            "items",
            []
        )
    )

    return [
        {
            "id": album.get("id"),

            "name": album.get("name"),

            "artist": (
                album.get(
                    "artists",
                    [{}]
                )[0].get("name")
            ),

            "release_date": album.get(
                "release_date"
            ),

            "uri": album.get("uri")
        }

        for album in albums
    ]


def search_playlist(query, limit=SEARCH_LIMIT):
    """
    Search Spotify playlists.
    """

    results = safe_search(
        query,
        "playlist",
        limit
    )

    playlists = (
        results.get(
            "playlists",
            {}
        ).get(
            "items",
            []
        )
    )

    return [
        {
            "id": playlist.get("id"),

            "name": playlist.get("name"),

            "owner": (
                playlist.get(
                    "owner",
                    {}
                ).get(
                    "display_name"
                )
            ),

            "uri": playlist.get("uri")
        }

        for playlist in playlists
    ]