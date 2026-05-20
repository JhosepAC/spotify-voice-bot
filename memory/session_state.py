class SessionState:

    def __init__(self):

        self.current_track = None

        self.current_artist = None

        self.current_album = None

        self.current_playlist = None

        self.last_intent = None

    def reset(self):
        """
        Reset session state.
        """

        self.current_track = None

        self.current_artist = None

        self.current_album = None

        self.current_playlist = None

        self.last_intent = None