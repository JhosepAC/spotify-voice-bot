import time

import numpy as np

import sounddevice as sd

from voice.audio_config import (
    SAMPLE_RATE,
    CHANNELS,
    CHUNK_SIZE,
    MAX_SILENCE_SECONDS
)

from voice.vad_detector import (
    is_speech
)

from voice.audio_buffer import (
    AudioBuffer
)

from voice.audio_preprocessor import (
    normalize_audio,
    remove_noise
)


class StreamingListener:

    def __init__(self):

        self.buffer = AudioBuffer()

    def listen(self):
        """
        Listen natural speech.
        """

        silence_start = None

        started = False

        with sd.InputStream(

            samplerate=SAMPLE_RATE,

            channels=CHANNELS,

            blocksize=CHUNK_SIZE,

            dtype="float32"

        ) as stream:

            print("Listening...")

            while True:

                chunk, _ = stream.read(
                    CHUNK_SIZE
                )

                chunk = chunk.flatten()

                speech_detected = (
                    is_speech(chunk)
                )

                if speech_detected:

                    started = True

                    silence_start = None

                    self.buffer.add(chunk)

                elif started:

                    self.buffer.add(chunk)

                    if silence_start is None:

                        silence_start = (
                            time.time()
                        )

                    silence_duration = (
                        time.time()
                        -
                        silence_start
                    )

                    if (
                        silence_duration
                        >=
                        MAX_SILENCE_SECONDS
                    ):
                        break

        audio = np.concatenate(
            self.buffer.get_audio()
        )

        self.buffer.clear()

        audio = normalize_audio(
            audio
        )

        audio = remove_noise(
            audio
        )

        return audio