class AudioBuffer:

    def __init__(self):

        self.frames = []

    def add(self, chunk):
        """
        Add audio chunk.
        """

        self.frames.append(chunk)

    def clear(self):
        """
        Clear buffer.
        """

        self.frames = []

    def get_audio(self):
        """
        Get complete audio.
        """

        return self.frames