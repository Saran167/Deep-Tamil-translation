def calculate_confidence(total_words, matched_words):
    if total_words == 0:
        return 0

    score = (matched_words / total_words) * 100
    return round(score, 2)
