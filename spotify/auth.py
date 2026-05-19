import os

from dotenv import load_dotenv

import spotipy

from spotipy.oauth2 import SpotifyOAuth


load_dotenv()


SPOTIFY_CLIENT_ID = os.getenv(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = os.getenv(
    "SPOTIFY_CLIENT_SECRET"
)

SPOTIFY_REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI"
)


SPOTIFY_SCOPE = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-modify "
    "user-library-read"
)

def create_spotify_client():
    """
    Create authenticated Spotify client.
    """

    auth_manager = SpotifyOAuth(

        client_id=SPOTIFY_CLIENT_ID,

        client_secret=SPOTIFY_CLIENT_SECRET,

        redirect_uri=SPOTIFY_REDIRECT_URI,

        scope=SPOTIFY_SCOPE,

        open_browser=True
    )

    spotify_client = spotipy.Spotify(
        auth_manager=auth_manager
    )

    return spotify_client

sp = create_spotify_client()

def get_spotify_client():
    """
    Return Spotify client instance.
    """

    return sp