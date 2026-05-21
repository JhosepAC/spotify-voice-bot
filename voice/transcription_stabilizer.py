"""
Transcription stabilizer.
Cleans and validates Whisper output before NLP processing.
"""

import re


MIN_COMMAND_LENGTH = 3

_GARBAGE_EXACT = {
    "eh", "ah", "hm", "hmm", "mmm", "mm", "uh", "huh",
    "gracias", "okay", "ok", "sí", "no", "...", ".",
    "subtítulos por la comunidad de amara.org",
    "subtítulos realizados por la comunidad de amara.org",
}

_GARBAGE_RE = re.compile(
    r'^(transcri|subtítulo|amara|suscríbete|like y suscríbete)',
    re.I
)


def normalize_text(text: str) -> str:
    """
    Normalize transcription: lowercase, strip, clean punctuation.
    Preserves apostrophes and hyphens useful in names.
    """
    text = text.strip()
    text = re.sub(r"[^\w\s'\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_invalid_transcription(text: str) -> bool:
    """
    Returns True if the text looks like garbage / hallucination.
    """
    if not text:
        return True

    if len(text) < MIN_COMMAND_LENGTH:
        return True

    if text.lower() in _GARBAGE_EXACT:
        return True

    if _GARBAGE_RE.search(text):
        return True

    if len(set(text.replace(" ", ""))) < 3:
        return True

    return False


def stabilize_transcription(text: str) -> str:
    """
    Normalize and validate transcribed text.

    Returns:
        Clean text string, or empty string if invalid.
    """
    normalized = normalize_text(text)

    if is_invalid_transcription(normalized):
        return ""

    return normalized
