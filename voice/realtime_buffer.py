import numpy as np


class RealtimeBuffer:

    def __init__(self):

        self.frames = []

    def add_chunk(self, chunk):
        """
        Add audio chunk.
        """

        self.frames.append(chunk)

    def clear(self):
        """
        Clear audio buffer.
        """

        self.frames = []

    def get_audio(self):
        """
        Get buffered audio.
        """

        if not self.frames:
            return None

        return np.concatenate(
            self.frames,
            axis=0
        )