import numpy as np


class AudioBuffer:

    def __init__(self):

        self.frames = []

    def add(
        self,
        chunk: np.ndarray
    ):
        """
        Add audio chunk.
        """

        self.frames.append(chunk)

    def clear(self):
        """
        Clear buffer.
        """

        self.frames.clear()

    def get_audio(self):
        """
        Return merged audio buffer.
        """

        if len(self.frames) == 0:

            return np.array(
                [],
                dtype=np.float32
            )

        return np.concatenate(
            self.frames
        ).astype(np.float32)