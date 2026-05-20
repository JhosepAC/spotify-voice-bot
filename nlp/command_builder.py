from nlp.intent_classifier import (
    classify_intent
)

from nlp.entity_extractor import (
    extract_entities
)


def build_command(text):
    """
    Build semantic command.
    """

    intent = classify_intent(
        text
    )

    entities = extract_entities(

        text,

        intent
    )

    return {
        "intent": intent,
        "entities": entities
    }