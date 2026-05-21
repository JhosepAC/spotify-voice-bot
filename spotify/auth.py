"""
Spotify OAuth authentication via Spotipy.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config.settings import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_SCOPES,
    SPOTIFY_CACHE_PATH,
)

_client: spotipy.Spotify | None = None


def get_spotify_client() -> spotipy.Spotify:
    """
    Returns authenticated Spotify client (singleton).
    """
    global _client

    if _client is None:
        auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPES,
            cache_path=SPOTIFY_CACHE_PATH,
            open_browser=True,
        )
        _client = spotipy.Spotify(auth_manager=auth_manager)

    return _client
