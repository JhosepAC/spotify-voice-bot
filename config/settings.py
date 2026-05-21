from dotenv import load_dotenv
import os
from pathlib import Path

# ─── Load .env ────────────────────────────────────────────────────────────────
load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"

# ─── Spotify ──────────────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
SPOTIFY_SCOPES = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-modify "
    "user-library-read "
    "playlist-read-private"
)
SPOTIFY_CACHE_PATH = ".spotify_cache"

# ─── Audio ────────────────────────────────────────────────────────────────────
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# ─── Whisper ──────────────────────────────────────────────────────────────────
WHISPER_MODEL = "medium"
WHISPER_LANGUAGE = "es"

# ─── TTS ──────────────────────────────────────────────────────────────────────
TTS_RATE = 165
TTS_VOLUME = 1.0

# ─── Ollama ───────────────────────────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")

# ─── Directories ──────────────────────────────────────────────────────────────
TEMP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
