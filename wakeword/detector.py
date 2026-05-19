WAKE_WORDS = [
    "spotify",
    "hey spotify",
    "ok spotify"
]

def detect_wake_word(text):
    """
    Detect wake word from text.
    """

    text = text.lower()

    for wake_word in WAKE_WORDS:

        if wake_word in text:
            return True

    return False