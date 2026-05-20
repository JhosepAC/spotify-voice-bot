import time

import numpy as np

from voice.whisper_engine import (
    transcribe_audio
)


class IncrementalTranscriber:
    """
    Incremental realtime transcription engine.
    """

    def __init__(self):

        self.audio_buffer = []

        self.partial_text = ""

        self.last_transcription_time = 0

        self.transcription_interval = 0.8

    def add_audio(
        self,
        chunk: np.ndarray
    ):
        """
        Add audio chunk.
        """

        self.audio_buffer.extend(
            chunk
        )

    def should_transcribe(self):
        """
        Check if partial transcription
        should execute.
        """

        current_time = time.time()

        elapsed = (
            current_time
            - self.last_transcription_time
        )

        return (
            elapsed
            >= self.transcription_interval
        )

    def get_partial_transcription(self):
        """
        Generate partial transcription.
        """

        if len(self.audio_buffer) == 0:

            return ""

        audio_array = np.array(

            self.audio_buffer,

            dtype=np.float32
        )

        if len(audio_array) < 16000:

            return ""

        text = transcribe_audio(
            audio_array
        )

        self.partial_text = text

        self.last_transcription_time = (
            time.time()
        )

        return text

    def finalize(self):
        """
        Final transcription.
        """

        if len(self.audio_buffer) == 0:

            return ""

        audio_array = np.array(

            self.audio_buffer,

            dtype=np.float32
        )

        final_text = transcribe_audio(
            audio_array
        )

        self.reset()

        return final_text

    def reset(self):
        """
        Reset transcription state.
        """

        self.audio_buffer = []

        self.partial_text = ""

        self.last_transcription_time = 0