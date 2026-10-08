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
AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))
AUDIO_DTYPE = os.getenv("AUDIO_DTYPE", "float32")

# ─── Whisper ──────────────────────────────────────────────────────────────────
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
WHISPER_MODEL_SIZE = WHISPER_MODEL
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "es")
WHISPER_BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", "1"))
WHISPER_BEST_OF = int(os.getenv("WHISPER_BEST_OF", "1"))
WHISPER_TEMPERATURE = float(os.getenv("WHISPER_TEMPERATURE", "0.0"))
DEBUG_TRANSCRIPTION = os.getenv("DEBUG_TRANSCRIPTION", "true").lower() == "true"

# ─── Audio capture / VAD ──────────────────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
PRE_SPEECH_BUFFER_SIZE = int(os.getenv("PRE_SPEECH_BUFFER_SIZE", "8"))
MIN_ACTIVATION_FRAMES = int(os.getenv("MIN_ACTIVATION_FRAMES", "3"))
MAX_SILENCE_DURATION = float(os.getenv("MAX_SILENCE_DURATION", "1.4"))
MAX_RECORDING_SECONDS = float(os.getenv("MAX_RECORDING_SECONDS", "12"))
MIN_SPEECH_DURATION = float(os.getenv("MIN_SPEECH_DURATION", "0.3"))
BASE_ENERGY_THRESHOLD = float(os.getenv("BASE_ENERGY_THRESHOLD", "0.003"))
DYNAMIC_ENERGY_RATIO = float(os.getenv("DYNAMIC_ENERGY_RATIO", "1.5"))
NOISE_FLOOR_ALPHA = float(os.getenv("NOISE_FLOOR_ALPHA", "0.95"))
DEBUG_VAD = os.getenv("DEBUG_VAD", "false").lower() == "true"

# ─── TTS ──────────────────────────────────────────────────────────────────────
TTS_RATE = 165
TTS_VOLUME = 1.0

# ─── Ollama ───────────────────────────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "15"))
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"

# ─── Ducking (lower music while listening) ────────────────────────────────────
DUCKING_ENABLED = os.getenv("DUCKING_ENABLED", "true").lower() == "true"
DUCKING_LEVEL = int(os.getenv("DUCKING_LEVEL", "10"))

# ─── Telemetry ──────────────────────────────────────────────────────────────────
TELEMETRY_ENABLED = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
SAVE_AUDIO = os.getenv("SAVE_AUDIO", "true").lower() == "true"

# ─── Spotify network ──────────────────────────────────────────────────────────
SPOTIFY_TIMEOUT = int(os.getenv("SPOTIFY_TIMEOUT", "10"))

# ─── Slow-action acknowledgement ──────────────────────────────────────────────
SLOW_ACK_ENABLED = os.getenv("SLOW_ACK_ENABLED", "true").lower() == "true"
SLOW_ACK_SECONDS = float(os.getenv("SLOW_ACK_SECONDS", "1.2"))

# ─── Directories ──────────────────────────────────────────────────────────────
TEMP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
