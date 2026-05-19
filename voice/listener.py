import tempfile

import sounddevice as sd

from scipy.io.wavfile import write


SAMPLE_RATE = 44100

DURATION = 5


def record_audio():
    """
    Record command audio.
    """

    print("Listening command...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    write(
        temp_file.name,
        SAMPLE_RATE,
        recording
    )

    return temp_file.name