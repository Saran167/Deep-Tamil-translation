import re

# Dictionary: bookish → spoken Tamil
WORD_MAP = {
    "ஆகின்றது": "ஆகுது",
    "இருக்கின்றது": "இருக்கு",
    "சென்றார்": "போனார்",
    "சென்றது": "போச்சு",
    "வந்தார்": "வந்தாங்க",
    "மிகவும்": "ரொம்ப",
    "அதனால்": "அதனால",
    "எனவே": "அதனால",
    "பயன்படுத்தப்படுகிறது": "பயன்படுத்துறாங்க",
    "உள்ளது": "இருக்கு",
    "உள்ளனர்": "இருக்காங்க"
}

def split_sentences(text):
    # Split using Tamil full stop or English full stop
    sentences = re.split(r"[.!?।]", text)
    return [s.strip() for s in sentences if s.strip()]

def simplify_sentence(sentence):
    simplified = sentence
    for bookish, spoken in WORD_MAP.items():
        simplified = simplified.replace(bookish, spoken)
    return simplified

def simple_tamil(text):
    sentences = split_sentences(text)
    simplified_sentences = []

    for s in sentences:
        simplified_sentences.append(simplify_sentence(s))

    return " । ".join(simplified_sentences)

def people_friendly_tamil(text):
    # For now, same as simple_tamil
    # Later we can add tone changes
    return simple_tamil(text)

