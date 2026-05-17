from dotenv import load_dotenv
import os
from pathlib import Path

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()

# =========================
# BASE PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / "temp"

LOGS_DIR = BASE_DIR / "logs"

# =========================
# SPOTIFY CONFIG
# =========================

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")

SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_SCOPES = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-library-modify "
    "user-library-read"
)

SPOTIFY_CACHE_PATH = ".spotify_cache"

# =========================
# AUDIO CONFIG
# =========================

AUDIO_SAMPLE_RATE = 44100

AUDIO_CHANNELS = 1

AUDIO_DURATION = 5

AUDIO_FILENAME = TEMP_DIR / "audio.wav"

# =========================
# WHISPER CONFIG
# =========================

WHISPER_MODEL = "base"

WHISPER_LANGUAGE = "es"

# =========================
# TEXT TO SPEECH CONFIG
# =========================

TTS_RATE = 175

TTS_VOLUME = 1.0

# =========================
# CREATE REQUIRED DIRECTORIES
# =========================

TEMP_DIR.mkdir(exist_ok=True)

LOGS_DIR.mkdir(exist_ok=True)