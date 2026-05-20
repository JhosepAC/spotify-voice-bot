from nlp.intent_classifier import (
    classify_intent
)

from nlp.entity_extractor import (
    extract_track_name
)

from commands.intents import (
    PLAY_TRACK
)


def build_command(text):
    """
    Build semantic command.
    """

    intent = classify_intent(
        text
    )

    entities = {}

    if intent == PLAY_TRACK:

        entities["track_name"] = (
            extract_track_name(text)
        )

    return {
        "intent": intent,
        "entities": entities
    }