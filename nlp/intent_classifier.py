from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST,
    PAUSE,
    RESUME,
    NEXT_TRACK,
    PREVIOUS_TRACK,
    LIKE_SONG
)

from nlp.semantic_patterns import (
    ARTIST_PATTERNS,
    PAUSE_PATTERNS,
    RESUME_PATTERNS,
    NEXT_PATTERNS,
    PREVIOUS_PATTERNS,
    LIKE_PATTERNS
)


def contains_pattern(
    text,
    patterns
):
    """
    Semantic pattern detection.
    """

    return any(

        pattern in text

        for pattern in patterns
    )


def classify_intent(text):
    """
    Semantic intent classification.
    """

    text = text.lower()

    if contains_pattern(
        text,
        ARTIST_PATTERNS
    ):
        return PLAY_ARTIST

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
        PREVIOUS_PATTERNS
    ):
        return PREVIOUS_TRACK

    if contains_pattern(
        text,
        LIKE_PATTERNS
    ):
        return LIKE_SONG

    return PLAY_TRACK