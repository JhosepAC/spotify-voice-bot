import tempfile

import sounddevice as sd
import soundfile as sf


SAMPLE_RATE = 16000

CHANNELS = 1

DTYPE = "float32"


def record_audio(duration=5):
    """
    Record microphone audio.
    """

    print("Listening...")

    recording = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype=DTYPE
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