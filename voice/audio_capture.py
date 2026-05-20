import tempfile
import os
import sounddevice as sd
import soundfile as sf
from utils.logger import logger

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"

# Obtener dispositivo desde .env o usar el por defecto (None)
INPUT_DEVICE = os.getenv("MICROPHONE_ID")
if INPUT_DEVICE:
    INPUT_DEVICE = int(INPUT_DEVICE)

def record_audio(duration=5):
    """
    Record microphone audio.
    """
    logger.info(f"Grabando audio (Dispositivo: {INPUT_DEVICE if INPUT_DEVICE is not None else 'Default'})...")

    recording = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE,
        device=INPUT_DEVICE
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    sf.write(
        temp_file.name,
        recording,
        SAMPLE_RATE
    )

    return temp_file.name