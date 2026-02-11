# Archaeological Tamil dictionary with metadata

INSCRIPTION_DICT = {
    "ஊரிற்": {
        "modern": "ஊரில்",
        "meaning": "in the town",
        "origin": "Classical Tamil suffix"
    },
    "புகுந்தான்": {
        "modern": "நுழைந்தான்",
        "meaning": "entered",
        "origin": "Sangam usage"
    },
    "வேந்தன்": {
        "modern": "அரசன்",
        "meaning": "king",
        "origin": "Sangam literature"
    },
    "மன்னன்": {
        "modern": "அரசன்",
        "meaning": "king",
        "origin": "Ancient royal title"
    },
    "நகர்": {
        "modern": "நகரம்",
        "meaning": "city",
        "origin": "Classical Tamil"
    }
}

def convert_ancient_text(text):
    words = text.split()
    modern_words = []
    detected_terms = []

    for word in words:
        if word in INSCRIPTION_DICT:
            data = INSCRIPTION_DICT[word]
            modern_words.append(data["modern"])
            detected_terms.append({
                "ancient": word,
                "modern": data["modern"],
                "meaning": data["meaning"],
                "origin": data["origin"]
            })
        else:
            modern_words.append(word)

    return " ".join(modern_words), detected_terms

