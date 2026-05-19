from rapidfuzz import fuzz


SIMILARITY_THRESHOLD = 65



def similarity_score(text1, text2):
    """
    Calculate semantic similarity.
    """

    return fuzz.token_sort_ratio(
        text1.lower(),
        text2.lower()
    )



def find_best_match(query, candidates):
    """
    Find best semantic candidate.
    """

    best_candidate = None

    best_score = 0

    for candidate in candidates:

        score = similarity_score(
            query,
            candidate
        )

        if score > best_score:

            best_candidate = candidate

            best_score = score

    if best_score >= SIMILARITY_THRESHOLD:

        return best_candidate

    return None