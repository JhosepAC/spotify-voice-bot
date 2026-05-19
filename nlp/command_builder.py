from nlp.intent_classifier import (
    classify_intent
)

from nlp.entity_extractor import (
    extract_track_name,
    extract_artist_name
)

from commands.intents import (
    PLAY_TRACK,
    PLAY_ARTIST
)

from semantic.spotify_matcher import (
    resolve_track,
    resolve_artist
)



def build_command(text):
    """
    Build semantic command.
    """

    intent = classify_intent(text)

    entities = {}

    if intent == PLAY_TRACK:

        track_name = extract_track_name(
            text
        )

        resolved_track = resolve_track(
            track_name
        )

        entities[
            "track_name"
        ] = resolved_track

    elif intent == PLAY_ARTIST:

        artist_name = extract_artist_name(
            text
        )

        resolved_artist = resolve_artist(
            artist_name
        )

        entities[
            "artist_name"
        ] = resolved_artist

    return {
        "intent": intent,
        "entities": entities
    }