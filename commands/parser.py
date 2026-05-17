from commands.detector import detect_intent

from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST,
    PLAY_ALBUM,
    PLAY_PLAYLIST
)

ENTITY_PREFIXES = {
    PLAY_TRACK: [
        "pon",
        "reproduce",
        "toca"
    ],

    PLAY_ARTIST: [
        "pon música de",
        "reproduce artista",
        "artista"
    ],

    PLAY_ALBUM: [
        "pon álbum",
        "reproduce álbum",
        "album"
    ],

    PLAY_PLAYLIST: [
        "pon playlist",
        "reproduce playlist",
        "playlist"
    ]
}

def extract_entity(text, intent):
    """
    Extract entity from user text.
    """

    prefixes = ENTITY_PREFIXES.get(
        intent,
        []
    )

    clean_text = text.lower()

    for prefix in prefixes:

        if prefix in clean_text:

            clean_text = clean_text.replace(
                prefix,
                ""
            )

    return clean_text.strip()

def parse_command(text):
    """
    Parse user command into intent + entities.

    Args:
        text (str)

    Returns:
        dict
    """

    intent = detect_intent(text)

    entities = {}

    if intent == PLAY_TRACK:

        entities["track_name"] = extract_entity(
            text,
            intent
        )

    elif intent == PLAY_ARTIST:

        entities["artist_name"] = extract_entity(
            text,
            intent
        )

    elif intent == PLAY_ALBUM:

        entities["album_name"] = extract_entity(
            text,
            intent
        )

    elif intent == PLAY_PLAYLIST:

        entities["playlist_name"] = extract_entity(
            text,
            intent
        )

    return {
        "intent": intent,
        "entities": entities
    }