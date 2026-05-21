"""
Audio and Whisper configuration constants.
"""

# ─── Whisper ───────────────────────────────────────────────────────────────────
WHISPER_MODEL_SIZE = "medium"

WHISPER_LANGUAGE = "es"

WHISPER_BEAM_SIZE = 3
WHISPER_BEST_OF = 1
WHISPER_TEMPERATURE = 0.0 

DEBUG_TRANSCRIPTION = True

# ─── Captura de audio ─────────────────────────────────────────────────────────
AUDIO_SAMPLE_RATE = 16000 
AUDIO_CHANNELS = 1
AUDIO_DTYPE = "float32"

# ─── VAD (Voice Activity Detection) ──────────────────────────────────────────
CHUNK_SIZE = 512
PRE_SPEECH_BUFFER_SIZE = 8
MIN_ACTIVATION_FRAMES = 2
MAX_SILENCE_DURATION = 0.9
MAX_RECORDING_SECONDS = 12
MIN_SPEECH_DURATION = 0.3

BASE_ENERGY_THRESHOLD = 0.003
DYNAMIC_ENERGY_RATIO = 1.5
NOISE_FLOOR_ALPHA = 0.95

DEBUG_VAD = False
