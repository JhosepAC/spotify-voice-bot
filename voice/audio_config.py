"""
Realtime audio configuration.
Optimized for:
- Faster Whisper
- Low latency
- Streaming speech recognition
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

CHUNK_DURATION_MS = 30

CHUNK_SIZE = int(
    SAMPLE_RATE * CHUNK_DURATION_MS / 1000
)


# =========================
# SPEECH DETECTION
# =========================

MIN_SPEECH_DURATION = 0.30

MAX_SILENCE_DURATION = 1.0

PRE_SPEECH_BUFFER = 0.5


# =========================
# ENERGY THRESHOLDS
# =========================

BASE_ENERGY_THRESHOLD = 0.015

DYNAMIC_THRESHOLD_MULTIPLIER = 1.5


# =========================
# AUDIO NORMALIZATION
# =========================

ENABLE_NORMALIZATION = True

ENABLE_NOISE_REDUCTION = True

ENABLE_GAIN_CONTROL = True


# =========================
# REALTIME PERFORMANCE
# =========================

LOW_LATENCY_MODE = True

MAX_RECORDING_SECONDS = 12


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