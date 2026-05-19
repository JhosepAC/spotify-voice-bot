import re


COMMON_FIXES = {

    "spotifai": "spotify",

    "spoty": "spotify",

    "spotyfy": "spotify"
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

    for wrong, correct in (
        COMMON_FIXES.items()
    ):

        text = text.replace(
            wrong,
            correct
        )

    return text.strip()