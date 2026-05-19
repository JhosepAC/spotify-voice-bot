class PredictionContext:

    def __init__(self):

        self.intent = None

        self.entities = {}

        self.confidence = 0

        self.partial_text = ""

    def update(
        self,
        intent=None,
        entities=None,
        confidence=0,
        partial_text=""
    ):
        """
        Update prediction state.
        """

        if intent is not None:
            self.intent = intent

        if entities is not None:
            self.entities = entities

        self.confidence = confidence

        self.partial_text = partial_text

    def clear(self):
        """
        Reset prediction context.
        """

        self.intent = None

        self.entities = {}

        self.confidence = 0

        self.partial_text = ""