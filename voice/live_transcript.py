class LiveTranscript:

    def __init__(self):

        self.current_text = ""

    def update(self, text):
        """
        Update transcript.
        """

        self.current_text = text

    def append(self, text):
        """
        Append transcript.
        """

        self.current_text += (
            " " + text
        )

    def get(self):
        """
        Get transcript.
        """

        return self.current_text.strip()

    def clear(self):
        """
        Clear transcript.
        """

        self.current_text = ""