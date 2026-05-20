from prediction.intent_predictor import (
    predict_intent
)

from prediction.semantic_predictor import (
    predict_entities
)

from prediction.spotify_preloader import (
    SpotifyPreloader
)

from prediction.prediction_context import (
    PredictionContext
)


class CommandPredictor:

    def __init__(self):

        self.context = (
            PredictionContext()
        )

        self.preloader = (
            SpotifyPreloader()
        )

    def process_partial_text(
        self,
        partial_text
    ):
        """
        Predict command realtime.
        """

        intent_result = predict_intent(
            partial_text
        )

        intent = intent_result[
            "intent"
        ]

        confidence = intent_result[
            "confidence"
        ]

        entities = predict_entities(
            partial_text,
            intent
        )

        self.context.update(

            intent=intent,

            entities=entities,

            confidence=confidence,

            partial_text=partial_text
        )

        if (
            intent == "PLAY_TRACK"
            and
            confidence > 0.5
        ):

            track_name = (
                entities.get(
                    "track_name"
                )
            )

            self.preloader.preload_track(
                track_name
            )

        return self.context