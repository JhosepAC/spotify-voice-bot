from commands.intents import (
    PLAY_ARTIST,
    PLAY_ALBUM,
    PLAY_PLAYLIST,
    PLAY_TRACK,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG,
    REPEAT_LAST,
    UNKNOWN
)

INTENT_KEYWORDS = {

    PLAY_PLAYLIST: [
        "playlist",
        "lista"
    ],

    PLAY_ALBUM: [
        "álbum",
        "album"
    ],

    REPEAT_LAST: [
        "otra vez",
        "repite",
        "repetir"
    ],

    PLAY_TRACK: [
        "pon",
        "reproduce",
        "toca"
    ],

    PLAY_ARTIST: [
        "artista",
        "música de",
        "canciones de"
    ],

    PAUSE: [
        "pausa",
        "pausar",
        "detén"
    ],

    RESUME: [
        "reanuda",
        "continúa"
    ],

    NEXT_TRACK: [
        "siguiente",
        "next"
    ],

    PREVIOUS_TRACK: [
        "anterior",
        "retrocede"
    ],

    LIKE_SONG: [
        "like",
        "me gusta"
    ],
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