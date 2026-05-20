"""
Realtime audio configuration.
Ultra optimized low latency voice engine.
"""


# =========================
# AUDIO
# =========================

SAMPLE_RATE = 16000

CHANNELS = 1

DTYPE = "float32"


# =========================
# STREAMING
# =========================

CHUNK_DURATION_MS = 20

CHUNK_SIZE = int(
    SAMPLE_RATE * CHUNK_DURATION_MS / 1000
)


# =========================
# SPEECH DETECTION
# =========================

MIN_SPEECH_DURATION = 0.20

MAX_SILENCE_DURATION = 0.45

MIN_ACTIVATION_FRAMES = 3

END_SPEECH_FRAMES = 8

PRE_SPEECH_BUFFER_SIZE = 12


# =========================
# ENERGY
# =========================

BASE_ENERGY_THRESHOLD = 0.008

DYNAMIC_ENERGY_RATIO = 1.5

NOISE_FLOOR_ALPHA = 0.95


# =========================
# REALTIME
# =========================

LOW_LATENCY_MODE = True

MAX_RECORDING_SECONDS = 8


# =========================
# WHISPER
# =========================

WHISPER_MODEL_SIZE = "medium"

WHISPER_LANGUAGE = "es"

WHISPER_BEAM_SIZE = 1

WHISPER_BEST_OF = 1

WHISPER_TEMPERATURE = 0.0


# =========================
# DEBUG
# =========================

DEBUG_AUDIO = False

DEBUG_VAD = False

DEBUG_TRANSCRIPTION = True