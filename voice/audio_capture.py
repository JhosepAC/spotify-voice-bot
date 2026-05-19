import tempfile

import sounddevice as sd

import soundfile as sf

import numpy as np


SAMPLE_RATE = 16000


def record_audio(duration=5):
    """
    Record microphone audio.
    """

    print("Listening...")

    recording = sd.rec(
        int(duration * SAMPLE_RATE),

        samplerate=SAMPLE_RATE,

        channels=1,

        dtype="float32"
    )

    sd.wait()

    recording = np.squeeze(recording)

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