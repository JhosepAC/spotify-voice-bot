import tempfile

import sounddevice as sd

from scipy.io.wavfile import write

from wakeword.detector import (
    detect_wake_word
)

from voice.whisper_engine import (
    transcribe_audio
)


SAMPLE_RATE = 44100

DURATION = 3

def record_wake_audio():
    """
    Record short audio segment.
    """

    print("Listening wake word...")

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

def wait_for_wake_word():
    """
    Wait until wake word is detected.
    """

    while True:

        try:

            audio_file = record_wake_audio()

            text = transcribe_audio(
                audio_file
            )

            if not text:
                continue

            text = text.lower()

            print(f"Heard: {text}")

            if detect_wake_word(text):

                print(
                    "Wake word detected"
                )

                return True

        except Exception as error:

            print(error)