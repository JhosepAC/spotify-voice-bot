import re


COMMON_CORRECTIONS = {

    "spoty": "spotify",

    "spotifye": "spotify",

    "spotifai": "spotify",

    "blending lights": "blinding lights",

    "the weekend": "the weeknd",

    "daf pong": "daft punk",

    "eminemm": "eminem"
}

def optimize_transcript(text):
    """
    Optimize transcript text.
    """

    text = text.lower()

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

    for wrong, correct in COMMON_CORRECTIONS.items():

        text = text.replace(
            wrong,
            correct
        )

    return text.strip()