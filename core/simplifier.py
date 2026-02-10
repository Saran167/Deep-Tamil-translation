import re

# Bookish Tamil → Spoken Tamil
WORD_MAP = {
    "ஆகின்றது": "ஆகுது",
    "இருக்கின்றது": "இருக்கு",
    "உள்ளது": "இருக்கு",
    "உள்ளனர்": "இருக்காங்க",
    "சென்றார்": "போனார்",
    "சென்றது": "போச்சு",
    "வந்தார்": "வந்தாங்க",
    "வந்தது": "வந்துச்சு",
    "மிகவும்": "ரொம்ப",
    "அதனால்": "அதனால",
    "எனவே": "அதனால",
    "பயன்படுத்தப்படுகிறது": "பயன்படுத்துறாங்க",
    "நடத்தப்பட்டது": "நடத்தினாங்க",
    "ஆராய்ச்சி": "ரிசர்ச்",
    "மாணவர்கள்": "ஸ்டூடன்ட்ஸ்",
    "பேராசிரியர்": "ப்ரொஃபஸர்"
}

def split_sentences(text):
    sentences = re.split(r"[.!?।]", text)
    return [s.strip() for s in sentences if s.strip()]

def simplify_sentence(sentence):
    simplified = sentence
    for bookish, spoken in WORD_MAP.items():
        simplified = simplified.replace(bookish, spoken)

    # Make sentence shorter & friendly
    simplified = simplified.replace("என்பது", "")
    simplified = simplified.strip()

    return simplified

def simple_tamil(text):
    sentences = split_sentences(text)
    simplified_sentences = []

    for s in sentences:
        simplified_sentences.append(simplify_sentence(s))

    return " । ".join(simplified_sentences)

def people_friendly_tamil(text):
    # Add friendly ending tone
    friendly = simple_tamil(text)
    return friendly


