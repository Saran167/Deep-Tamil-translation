# Ancient / Archaeological Tamil → Modern Tamil

ANCIENT_WORD_MAP = {
    "ஊரிற்": "ஊரில்",
    "ஊரின்": "ஊரின்",
    "புகுந்தான்": "நுழைந்தான்",
    "சென்றான்": "போனான்",
    "வந்தான்": "வந்தான்",
    "இருந்தான்": "இருந்தான்",
    "கொண்டான்": "எடுத்தான்",
    "மகன்": "மகன்",
    "மகள்": "மகள்",
    "மன்னன்": "அரசன்",
    "வேந்தன்": "அரசன்",
    "படை": "ராணுவம்",
    "நகர்": "நகரம்"
}

SUFFIX_RULES = {
    "ஆன்": "ஆன்",
    "ஆள்": "ஆள்",
    "இன்": "இன்",
    "இல்": "இல்",
    "உம்": "உம்"
}

def ancient_to_modern(text):
    words = text.split()
    modern_words = []

    for word in words:
        # Direct word mapping
        if word in ANCIENT_WORD_MAP:
            modern_words.append(ANCIENT_WORD_MAP[word])
        else:
            modern_words.append(word)

    return " ".join(modern_words)
