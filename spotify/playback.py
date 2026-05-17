from spotify.auth import get_spotify_client
from spotify.device import validate_active_device

from spotify.search import (
    search_track,
    search_artist,
    search_album,
    search_playlist
)

sp = get_spotify_client()


# =========================
# PLAYBACK CONTROL FUNCTIONS
# =========================
# These functions control Spotify playback. They first validate that there is an active Spotify device, and then call the appropriate Spotify API method.

# The play_track function searches for a track by name and plays it if found.
def play_track(track_name):
    """
    Search and play a Spotify track.

    Args:
        track_name (str)

    Returns:
        dict | None
    """

    validate_active_device()

    tracks = search_track(track_name)

    if not tracks:
        return None

    track = tracks[0]

    sp.start_playback(
        uris=[track["uri"]]
    )

    return track

# The play_artist function searches for an artist by name and plays their top tracks if found.
def play_artist(artist_name):
    """
    Search and play Spotify artist.
    """

    validate_active_device()

    artists = search_artist(artist_name)

    if not artists:
        return None

    artist = artists[0]

    sp.start_playback(
        context_uri=artist["uri"]
    )

    return artist

# The play_album function searches for an album by name and plays it if found.
def play_album(album_name):
    """
    Search and play Spotify album.
    """

    validate_active_device()

    albums = search_album(album_name)

    if not albums:
        return None

    album = albums[0]

    sp.start_playback(
        context_uri=album["uri"]
    )

    return album

# The play_playlist function searches for a playlist by name and plays it if found.
def play_playlist(playlist_name):
    """
    Search and play Spotify playlist.
    """

    validate_active_device()

    playlists = search_playlist(playlist_name)

    if not playlists:
        return None

    playlist = playlists[0]

    sp.start_playback(
        context_uri=playlist["uri"]
    )

    return playlist