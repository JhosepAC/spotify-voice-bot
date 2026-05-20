import numpy as np
import scipy.signal
from typing import cast

from voice.audio_config import (
    SAMPLE_RATE,
    ENABLE_NORMALIZATION,
    ENABLE_NOISE_REDUCTION
)


class AudioPreprocessor:
    """
    Optimized preprocessing pipeline
    for realtime Whisper.
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
        Safe normalization.
        """

        if not ENABLE_NORMALIZATION:

            return audio

        peak = np.max(
            np.abs(audio)
        )

        if peak <= 1e-5:

            return audio

        gain = min(
            1.5,
            1.0 / peak
        )

        return audio * gain

    def reduce_noise(
        self,
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Basic noise reduction.
        """

        if not ENABLE_NOISE_REDUCTION:
            return audio

        if len(audio) < 32:
            return audio

        filtered = scipy.signal.sosfilt(
            self.sos,
            audio
        )

        return cast(np.ndarray, filtered)

    def trim_silence(
        self,
        audio: np.ndarray,
        threshold: float = 0.01
    ) -> np.ndarray:
        """
        Adaptive silence trimming.
        """

        if len(audio) == 0:

            return audio

        abs_audio = np.abs(audio)

        dynamic_threshold = max(

            threshold,

            np.mean(abs_audio) * 2
        )

        indices = np.where(
            abs_audio > dynamic_threshold
        )[0]

        if len(indices) == 0:

            return np.array(
                [],
                dtype=np.float32
            )

        start = indices[0]

        end = indices[-1]

        return audio[
            start:end + 1
        ]

    def process(
        self,
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Full preprocessing pipeline.
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

        audio = self.normalize(
            audio
        )

        audio = self.reduce_noise(
            audio
        )

        audio = self.trim_silence(
            audio
        )

        return audio