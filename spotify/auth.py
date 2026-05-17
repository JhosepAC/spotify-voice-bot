from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-modify "
    "user-library-read"
)

CACHE_PATH = ".spotify_cache"


def create_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=SCOPES,
        cache_path=CACHE_PATH,
        open_browser=True
    )

    return spotipy.Spotify(auth_manager=auth_manager)


sp = create_spotify_client()


def get_spotify_client():
    return sp