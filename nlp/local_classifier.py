"""Local fuzzy intent scorer (<100ms, no server).

Scores normalized input against paraphrase examples with RapidFuzz.
Used as the first NLU stage so common paraphrases resolve instantly.
LLM (Ollama) is only a fallback for low-confidence cases.
"""

from rapidfuzz import fuzz

from nlp.examples import INTENT_EXAMPLES
from nlp.normalizer import normalize

HIGH_CONFIDENCE = 86.0
CANDIDATE_CONFIDENCE = 68.0


def score_intent(text: str) -> dict:
    """Return {intent, confidence, score} for the best matching intent."""
    norm = normalize(text)
    if not norm:
        return {"intent": "UNKNOWN", "confidence": 0.0, "score": 0.0}

    best_intent = "UNKNOWN"
    best_score = 0.0
    runner_up = 0.0

    for intent, examples in INTENT_EXAMPLES.items():
        intent_best = 0.0
        for example in examples:
            score = float(fuzz.token_set_ratio(norm, example))
            if score > intent_best:
                intent_best = score
                if intent_best >= 100.0:
                    break
        if intent_best > best_score:
            runner_up = best_score
            best_score = intent_best
            best_intent = intent
        elif intent_best > runner_up:
            runner_up = intent_best

    margin = best_score - runner_up
    if best_score >= HIGH_CONFIDENCE and margin >= 5.0:
        confidence = min(0.95, 0.70 + best_score / 400.0)
    elif best_score >= CANDIDATE_CONFIDENCE:
        confidence = min(0.80, 0.50 + best_score / 400.0)
    else:
        return {"intent": "UNKNOWN", "confidence": best_score / 200.0, "score": best_score}

    return {"intent": best_intent, "confidence": round(confidence, 2), "score": round(best_score, 1)}
