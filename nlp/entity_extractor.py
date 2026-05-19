PLAY_PATTERNS = [

    "pon",

    "reproduce",

    "quiero escuchar",

    "ponme",

    "toca",

    "play"
]


ARTIST_PATTERNS = [

    "música de",

    "algo de",

    "artista",

    "songs by"
]



def clean_patterns(text, patterns):

    clean_text = text.lower()

    for pattern in patterns:

        clean_text = clean_text.replace(
            pattern,
            ""
        )

    return clean_text.strip()



def extract_track_name(text):
    """
    Extract track entity.
    """

    return clean_patterns(
        text,
        PLAY_PATTERNS
    )



def extract_artist_name(text):
    """
    Extract artist entity.
    """

    return clean_patterns(
        text,
        ARTIST_PATTERNS
    )