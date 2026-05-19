MIN_WORDS = 1


def validate_transcript(text):
    """
    Validate transcript quality.
    """

    if not text:
        return False

    words = text.split()

    if len(words) < MIN_WORDS:
        return False

    return True