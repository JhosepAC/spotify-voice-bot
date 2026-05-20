REFERENCE_WORDS = {

    "song": [
        "esa canción",
        "la canción",
        "agrégala",
        "likeala"
    ],

    "artist": [
        "ese artista",
        "el artista"
    ],

    "album": [
        "ese álbum",
        "el álbum"
    ]
}


def contains_reference(text):
    """
    Detect contextual references.
    """

    text = text.lower()

    for refs in (
        REFERENCE_WORDS.values()
    ):

        for ref in refs:

            if ref in text:
                return True

    return False