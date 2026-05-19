from semantic.spotify_matcher import (
    resolve_track,
    resolve_artist
)

from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST
)


def predict_entities(
    partial_text,
    intent
):
    """
    Predict entities from partial speech.
    """

    if not intent:
        return {}

    text = partial_text.lower()

    entities = {}

    if intent == PLAY_TRACK:

        for keyword in [
            "pon",
            "reproduce",
            "play"
        ]:

            text = text.replace(
                keyword,
                ""
            )

        predicted_track = (
            resolve_track(
                text.strip()
            )
        )

        entities[
            "track_name"
        ] = predicted_track

    elif intent == PLAY_ARTIST:

        predicted_artist = (
            resolve_artist(
                text.strip()
            )
        )

        entities[
            "artist_name"
        ] = predicted_artist

    return entities