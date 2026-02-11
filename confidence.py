def calculate_confidence(total_words, matched_words):
    if total_words == 0:
        return 0
    return round((matched_words / total_words) * 100, 2)
