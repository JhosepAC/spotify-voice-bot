from difflib import SequenceMatcher


def similarity_score(
    first,
    second
):
    """
    Calculate semantic similarity.
    """

    return SequenceMatcher(

        None,

        first.lower(),

        second.lower()

    ).ratio()


def find_best_match(
    query,
    candidates,
    threshold=0.55
):
    """
    Find best semantic candidate.
    """

    best_match = None

    best_score = 0.0

    for candidate in candidates:

        score = similarity_score(

            query,

            candidate
        )

        if score > best_score:

            best_score = score

            best_match = candidate

    if best_score < threshold:

        return None

    return best_match