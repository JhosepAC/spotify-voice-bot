from commands.intents import (
    PLAY_TRACK,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    LIKE_SONG
)

from nlp.semantic_patterns import (
    PLAY_PATTERNS,
    PAUSE_PATTERNS,
    RESUME_PATTERNS,
    NEXT_PATTERNS,
    LIKE_PATTERNS
)

def contains_pattern(text, patterns):

    for pattern in patterns:

        if pattern in text:
            return True

    return False

def classify_intent(text):
    """
    Detect semantic intent.
    """

    text = text.lower()

    if contains_pattern(
        text,
        PLAY_PATTERNS
    ):
        return PLAY_TRACK

    if contains_pattern(
        text,
        PAUSE_PATTERNS
    ):
        return PAUSE

    if contains_pattern(
        text,
        RESUME_PATTERNS
    ):
        return RESUME

    if contains_pattern(
        text,
        NEXT_PATTERNS
    ):
        return NEXT_TRACK

    if contains_pattern(
        text,
        LIKE_PATTERNS
    ):
        return LIKE_SONG

    return None