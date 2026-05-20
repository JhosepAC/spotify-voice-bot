from difflib import SequenceMatcher


def similarity_score(
    text_a,
    text_b
):
    """
    Calculate semantic similarity score.
    """

    return SequenceMatcher(

        None,

        text_a.lower(),

        text_b.lower()

    ).ratio()


def find_best_match(
    query,
    candidates
):
    """
    Find best semantic candidate.
    """

    if not candidates:

        return None

    best_candidate = None

    best_score = 0.0

    for candidate in candidates:

        candidate_name = candidate.get(
            "name",
            ""
        )

        score = similarity_score(

            query,

            candidate_name
        )

        if score > best_score:

            best_score = score

            best_candidate = candidate

    if best_score < 0.45:

        return None

    return best_candidate