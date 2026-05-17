from spotify.auth import get_spotify_client

sp = get_spotify_client()


def search_track(query, limit=1):
    """
    Search for a Spotify track.

    Args:
        query (str): track name
        limit (int): max results

    Returns:
        list[dict]
    """

    results = sp.search(
        q=query,
        type="track",
        limit=limit
    )

    tracks = results["tracks"]["items"]

    return [
        {
            "id": track.get("id"),
            "name": track.get("name"),
            "artist": (
                track.get("artists", [{}])[0].get("name")
            ),
            "album": (
                track.get("album", {}).get("name")
            ),
            "uri": track.get("uri")
        }
        for track in tracks
    ]


def search_artist(query, limit=1):
    """
    Search for a Spotify artist.
    """

    results = sp.search(
        q=query,
        type="artist",
        limit=limit
    )

    artists = results["artists"]["items"]

    return [
        {
            "id": artist.get("id"),
            "name": artist.get("name"),
            "genres": artist.get("genres", []),
            "followers": artist.get("followers", {}).get("total", 0),
            "uri": artist.get("uri")
        }
        for artist in artists
    ]


def search_album(query, limit=1):
    """
    Search for a Spotify album.
    """

    results = sp.search(
        q=query,
        type="album",
        limit=limit
    )

    albums = results["albums"]["items"]

    return [
        {
            "id": album.get("id"),
            "name": album.get("name"),
            "artist": (
                album.get("artists", [{}])[0].get("name")
            ),
            "release_date": album.get("release_date"),
            "uri": album.get("uri")
        }
        for album in albums
    ]


def search_playlist(query, limit=1):
    """
    Search for a Spotify playlist.
    """

    results = sp.search(
        q=query,
        type="playlist",
        limit=limit
    )

    playlists = results["playlists"]["items"]

    return [
        {
            "id": playlist.get("id"),
            "name": playlist.get("name"),
            "owner": (
                playlist.get("owner", {}).get("display_name")
            ),
            "uri": playlist.get("uri")
        }
        for playlist in playlists
    ]