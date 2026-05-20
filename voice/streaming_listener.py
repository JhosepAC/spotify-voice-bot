import collections
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
    DYNAMIC_ENERGY_RATIO,
    NOISE_FLOOR_ALPHA,
    MIN_ACTIVATION_FRAMES,
    END_SPEECH_FRAMES,
    PRE_SPEECH_BUFFER_SIZE,
    DEBUG_VAD,
    MAX_RECORDING_SECONDS
)

from voice.audio_preprocessor import (
    AudioPreprocessor
)


class StreamingListener:

    def __init__(self):

        self.sample_rate = SAMPLE_RATE

        self.chunk_size = CHUNK_SIZE

        self.channels = CHANNELS

        self.dtype = DTYPE

        self.preprocessor = (
            AudioPreprocessor()
        )

        self.noise_floor = (
            BASE_ENERGY_THRESHOLD
        )

    def calculate_energy(
        self,
        chunk
    ):
        """
        RMS energy.
        """

        return float(

            np.sqrt(

                np.mean(
                    np.square(chunk)
                )
            )
        )

    def update_noise_floor(
        self,
        energy
    ):
        """
        Adaptive environment learning.
        """

        self.noise_floor = (

            NOISE_FLOOR_ALPHA
            * self.noise_floor

            +

            (1 - NOISE_FLOOR_ALPHA)
            * energy
        )

    def get_dynamic_threshold(self):
        """
        Dynamic speech threshold.
        """

        return max(

            BASE_ENERGY_THRESHOLD,

            self.noise_floor
            * DYNAMIC_ENERGY_RATIO
        )

    def is_speech(
        self,
        chunk
    ):
        """
        Adaptive speech detection.
        """

        energy = self.calculate_energy(
            chunk
        )

        self.update_noise_floor(
            energy
        )

        threshold = (
            self.get_dynamic_threshold()
        )

        if DEBUG_VAD:

            print(
                f"Energy={energy:.6f} "
                f"Threshold={threshold:.6f}"
            )

        return energy > threshold

    def listen(self):
        """
        Ultra low latency streaming listener.
        """

        print("Listening...")

        audio_frames = []

        pre_speech_buffer = collections.deque(
            maxlen=PRE_SPEECH_BUFFER_SIZE
        )

        speech_started = False

        activation_frames = 0

        silence_frames = 0

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

                chunk = (
                    self.preprocessor.process(
                        chunk
                    )
                )

                if len(chunk) == 0:

                    continue

                current_time = time.time()

                speech_detected = (
                    self.is_speech(chunk)
                )

                if not speech_started:

                    pre_speech_buffer.append(
                        chunk
                    )

                    if speech_detected:

                        activation_frames += 1

                        if (
                            activation_frames
                            >= MIN_ACTIVATION_FRAMES
                        ):

                            speech_started = True

                            audio_frames.extend(
                                pre_speech_buffer
                            )

                            if DEBUG_VAD:

                                print(
                                    "Speech started"
                                )

                    else:

                        activation_frames = 0

                else:

                    audio_frames.append(
                        chunk
                    )

                    if speech_detected:

                        silence_frames = 0

                    else:

                        silence_frames += 1

                        silence_time = (

                            silence_frames

                            *

                            (
                                self.chunk_size
                                / self.sample_rate
                            )
                        )

                        if (
                            silence_time
                            >= MAX_SILENCE_DURATION
                        ):

                            if DEBUG_VAD:

                                print(
                                    "Speech ended"
                                )

                            break

                elapsed = (
                    current_time
                    - recording_start
                )

                if (
                    elapsed
                    >= MAX_RECORDING_SECONDS
                ):

                    break

        if len(audio_frames) == 0:

            return np.array(
                [],
                dtype=np.float32
            )

        audio = np.concatenate(
            audio_frames
        )

        duration = (
            len(audio)
            / self.sample_rate
        )

        if (
            duration
            < MIN_SPEECH_DURATION
        ):

            return np.array(
                [],
                dtype=np.float32
            )

        return audio