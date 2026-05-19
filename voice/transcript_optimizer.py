import re


COMMON_STRUCTURAL_FIXES = {

    "spotifai": "spotify",

    "spoty": "spotify",

    "spotifye": "spotify"
}



def optimize_transcript(text):
    """
    Optimize transcript structure.
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

    for wrong, correct in (
        COMMON_STRUCTURAL_FIXES.items()
    ):

        text = text.replace(
            wrong,
            correct
        )

    return text.strip()