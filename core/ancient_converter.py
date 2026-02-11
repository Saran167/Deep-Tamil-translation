INSCRIPTION_DICT = {
    "ஊரிற்": {
        "modern": "ஊரில்",
        "meaning": "in town",
        "origin": "Classical Tamil"
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
    }
}

def convert_ancient_text(text):
    words = text.split()
    modern_words = []
    detected = []

    for w in words:
        if w in INSCRIPTION_DICT:
            data = INSCRIPTION_DICT[w]
            modern_words.append(data["modern"])
            detected.append({
                "ancient": w,
                "modern": data["modern"],
                "meaning": data["meaning"],
                "origin": data["origin"]
            })
        else:
            modern_words.append(w)

    return " ".join(modern_words), detected


