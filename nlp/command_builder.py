"""
Build semantic command from transcribed text.
Single entry point: classify intent + extract entities in one call.
"""

from nlp.intent_classifier import classify_intent


def build_command(text: str) -> dict:
    """
    Parse text into intent + entities.

    Returns:
        {
            "intent": str | None,
            "entities": dict
        }
    """
    if not text or not text.strip():
        return {"intent": None, "entities": {}}

    result = classify_intent(text)

    intent = result.get("intent")
    entities = result.get("entities", {})
    confidence = result.get("confidence", 0.0)

    # Descarta resultados de baja confianza
    if confidence < 0.35 or intent == "UNKNOWN":
        intent = None

    return {
        "intent": intent,
        "entities": entities,
        "confidence": confidence,
    }
