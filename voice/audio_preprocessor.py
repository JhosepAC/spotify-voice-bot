import numpy as np

import scipy.signal

from typing import cast

from voice.audio_config import (
    SAMPLE_RATE
)


class AudioPreprocessor:
    """
    Ultra lightweight realtime audio preprocessor.
    Optimized for:
    - low latency
    - Whisper
    - realtime streaming
    """

    def __init__(self):

        self.sample_rate = SAMPLE_RATE

        cutoff = min(
            80,
            self.sample_rate * 0.01
        )

        self.sos = scipy.signal.butter(

            2,

            cutoff / (
                self.sample_rate / 2
            ),

            btype="highpass",

            output="sos"
        )

    def normalize(
        self,
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Lightweight normalization.
        """

        peak = np.max(
            np.abs(audio)
        )

        if peak <= 1e-5:

            return audio

        gain = min(
            1.2,
            1.0 / peak
        )

        return audio * gain

    def reduce_noise(
        self,
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Minimal realtime noise reduction.
        """

        if len(audio) < 32:

            return audio

        filtered = scipy.signal.sosfilt(

            self.sos,

            audio
        )

        return cast(
            np.ndarray,
            filtered
        )

    def process(
        self,
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Fast realtime preprocessing pipeline.
        """

        if (
            audio is None
            or len(audio) == 0
        ):

            return np.array(
                [],
                dtype=np.float32
            )

        audio = audio.astype(
            np.float32
        )

        # -------------------------
        # LIGHT NORMALIZATION
        # -------------------------

        audio = self.normalize(
            audio
        )

        # -------------------------
        # LIGHT NOISE FILTER
        # -------------------------

        audio = self.reduce_noise(
            audio
        )

        return audio