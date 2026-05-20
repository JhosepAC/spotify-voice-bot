from nlp.semantic_patterns import (
    PLAY_PATTERNS
)


def extract_track_name(text):
    """
    Extract music entity naturally.
    """

    clean_text = text.lower()

    for pattern in PLAY_PATTERNS:

        clean_text = clean_text.replace(
            pattern,
            ""
        )

    return clean_text.strip()