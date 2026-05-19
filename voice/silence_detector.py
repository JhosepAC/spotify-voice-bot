import time


class SilenceDetector:

    def __init__(self):

        self.last_voice_time = (
            time.time()
        )

    def update(self):

        self.last_voice_time = (
            time.time()
        )

    def silence_exceeded(
        self,
        timeout=1.5
    ):
        """
        Detect silence timeout.
        """

        return (

            time.time()
            -
            self.last_voice_time

        ) > timeout