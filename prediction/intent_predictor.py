from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST,
    PAUSE,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG
)


INTENT_PATTERNS = {

    PLAY_TRACK: [

        "pon",
        "reproduce",
        "toca",
        "play"
    ],

    PLAY_ARTIST: [

        "música de",
        "artista",
        "songs by"
    ],

    PAUSE: [

        "pausa",
        "pause",
        "detén"
    ],

    NEXT_TRACK: [

        "siguiente",
        "next"
    ],

    PREVIOUS_TRACK: [

        "anterior",
        "previous"
    ],

    LIKE_SONG: [

        "like",
        "me gusta",
        "guardar canción"
    ]
}


def predict_intent(partial_text):
    """
    Predict user intent from partial speech.
    """

    text = partial_text.lower()

    best_intent = None

    best_score = 0

    for intent, patterns in (
        INTENT_PATTERNS.items()
    ):

        for pattern in patterns:

            if pattern in text:

                score = len(pattern)

                if score > best_score:

                    best_intent = intent

                    best_score = score

    confidence = min(
        best_score / 10,
        1.0
    )

    return {
        "intent": best_intent,
        "confidence": confidence
    }