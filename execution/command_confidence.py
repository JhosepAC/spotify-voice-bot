def calculate_confidence(
    partial_text,
    intent,
    entities
):
    """
    Calculate execution confidence.
    """

    if not intent:
        return 0

    score = 0.0

    text_length = len(
        partial_text.split()
    )

    if text_length >= 2:
        score += 0.3

    if entities:
        score += 0.4

    if intent:
        score += 0.3

    return min(score, 1.0)