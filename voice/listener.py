import sounddevice as sd
from scipy.io.wavfile import write

from config.settings import (
    AUDIO_FILENAME,
    AUDIO_DURATION,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS
)


def record_audio():
    print("Grabando audio...")

    recording = sd.rec(
        int(AUDIO_DURATION * AUDIO_SAMPLE_RATE),
        samplerate=AUDIO_SAMPLE_RATE,
        channels=AUDIO_CHANNELS,
        dtype="int16"
    )

    sd.wait()

    write(
        AUDIO_FILENAME,
        AUDIO_SAMPLE_RATE,
        recording
    )

    print("Grabación finalizada")

    return str(AUDIO_FILENAME)