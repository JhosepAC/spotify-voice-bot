from commands.intents import (
    PLAY_TRACK,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG,
    UNKNOWN
)

INTENT_KEYWORDS = {
    PAUSE: [
        "pausa",
        "pausar",
        "detén",
        "detener",
        "para"
    ],

    RESUME: [
        "reanuda",
        "continúa",
        "seguir"
    ],

    NEXT_TRACK: [
        "siguiente",
        "next",
        "salta"
    ],

    PREVIOUS_TRACK: [
        "anterior",
        "retrocede",
        "previa"
    ],

    LIKE_SONG: [
        "like",
        "me gusta",
        "favorita",
        "guardar canción"
    ],

    PLAY_TRACK: [
        "pon",
        "reproduce",
        "toca"
    ]
}


def detect_intent(text):
    """
    Detect user intent from text.

    Args:
        text (str)

    Returns:
        str
    """

    text = text.lower()

    for intent, keywords in INTENT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:
                return intent

    return UNKNOWN