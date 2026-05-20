from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST
)

from nlp.semantic_patterns import (
    PLAY_TRACK_PATTERNS,
    ARTIST_PATTERNS
)


def clean_text(
    text,
    patterns
):
    """
    Remove semantic patterns.
    """

    for pattern in patterns:

        text = text.replace(
            pattern,
            ""
        )

    return text.strip()


def extract_entities(
    text,
    intent
):
    """
    Semantic entity extraction.
    """

    lower_text = text.lower()

    entities = {}

    # -------------------------
    # ARTIST DETECTION
    # -------------------------

    for pattern in ARTIST_PATTERNS:

        if pattern in lower_text:

            artist_name = lower_text.split(
                pattern
            )[-1].strip()

            if artist_name:

                entities["artist_name"] = (
                    artist_name
                )

                return entities

    # -------------------------
    # TRACK DETECTION
    # -------------------------

    if intent == PLAY_TRACK:

        track_name = clean_text(

            lower_text,

            PLAY_TRACK_PATTERNS
        )

        if track_name:

            entities["track_name"] = (
                track_name
            )

    return entities