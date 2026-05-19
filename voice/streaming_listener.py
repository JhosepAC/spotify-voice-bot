import time

import numpy as np

import sounddevice as sd

from voice.audio_config import (
    SAMPLE_RATE,
    CHANNELS,
    DTYPE,
    CHUNK_SIZE,
    MAX_SILENCE_DURATION,
    MIN_SPEECH_DURATION,
    BASE_ENERGY_THRESHOLD,
    DEBUG_VAD,
    MAX_RECORDING_SECONDS
)


class StreamingListener:

    def __init__(self):

        self.sample_rate = SAMPLE_RATE

        self.chunk_size = CHUNK_SIZE

        self.channels = CHANNELS

        self.dtype = DTYPE

        self.energy_threshold = (
            BASE_ENERGY_THRESHOLD
        )

    def calculate_audio_energy(
        self,
        audio_chunk
    ):
        """
        Calculate RMS energy.
        """

        return np.sqrt(
            np.mean(
                np.square(audio_chunk)
            )
        )

    def is_speech(
        self,
        audio_chunk
    ):
        """
        Detect speech activity.
        """

        energy = self.calculate_audio_energy(
            audio_chunk
        )

        if DEBUG_VAD:

            print(
                f"Energy: {energy:.6f}"
            )

        return (
            energy > self.energy_threshold
        )

    def listen(self):
        """
        Listen for realtime speech.
        """

        print(
            "Listening..."
        )

        audio_buffer = []

        speech_detected = False

        silence_start = None

        recording_start = time.time()

        with sd.InputStream(

            samplerate=self.sample_rate,

            channels=self.channels,

            dtype=self.dtype,

            blocksize=self.chunk_size

        ) as stream:

            while True:

                chunk, _ = stream.read(
                    self.chunk_size
                )

                chunk = chunk.flatten()

                current_time = time.time()

                if self.is_speech(chunk):

                    if not speech_detected:

                        speech_detected = True

                        if DEBUG_VAD:

                            print(
                                "Speech detected"
                            )

                    silence_start = None

                    audio_buffer.extend(
                        chunk
                    )

                elif speech_detected:

                    audio_buffer.extend(
                        chunk
                    )

                    if silence_start is None:

                        silence_start = (
                            current_time
                        )

                    silence_duration = (
                        current_time
                        - silence_start
                    )

                    if (
                        silence_duration
                        >= MAX_SILENCE_DURATION
                    ):

                        break

                if (
                    current_time
                    - recording_start
                    >= MAX_RECORDING_SECONDS
                ):

                    break

        if len(audio_buffer) == 0:

            return np.array(
                [],
                dtype=np.float32
            )

        audio_array = np.array(
            audio_buffer,
            dtype=np.float32
        )

        speech_duration = (
            len(audio_array)
            / self.sample_rate
        )

        if (
            speech_duration
            < MIN_SPEECH_DURATION
        ):

            return np.array(
                [],
                dtype=np.float32
            )

        return audio_array