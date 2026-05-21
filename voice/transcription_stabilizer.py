import re


MIN_COMMAND_LENGTH = 4


INVALID_WORDS = {

    "eh",
    "ah",
    "hm",
    "mmm",
    "bong",
    "po",
    "em",
    "mmm",
    "uh",
    "huh",
    "mm"
}


def normalize_text(text):
    """
    Normalize transcription text.
    """

    text = text.lower()

    text = text.strip()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def is_invalid_transcription(text):
    """
    Detect garbage transcriptions.
    """

    if not text:
        return True

    if len(text) < MIN_COMMAND_LENGTH:
        return True

    if text in INVALID_WORDS:
        return True

    return False


def stabilize_transcription(text):
    """
    Stabilize realtime transcription.
    """

    normalized = normalize_text(
        text
    )

    if is_invalid_transcription(
        normalized
    ):
        return ""

    return normalized