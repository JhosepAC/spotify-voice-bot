"""Text normalization for robust Spanish NLU.

Lowercases, strips accents, removes punctuation and extra spaces
so paraphrases match even with STT noise.
"""

import re
import unicodedata

_NON_WORD_RE = re.compile(r"[^\w\s'\-]", re.UNICODE)
_SPACES_RE = re.compile(r"\s+")


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def normalize(text: str) -> str:
    """Normalize user text for matching (accents/punct-insensitive)."""
    if not text:
        return ""
    text = text.lower().strip()
    text = strip_accents(text)
    text = _NON_WORD_RE.sub(" ", text)
    text = _SPACES_RE.sub(" ", text)
    return text.strip()
