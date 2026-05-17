from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv
import os

load_dotenv()

scope = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-modify "
    "user-library-read"
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=scope
    )
)

def get_spotify_client():
    return sp