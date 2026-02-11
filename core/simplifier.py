WORD_MAP = {
    "மிகவும்": "ரொம்ப",
    "எனவே": "அதனால",
    "ஆகின்றது": "ஆகுது",
    "இருக்கின்றது": "இருக்கு"
}

def simple_tamil(text):
    for k, v in WORD_MAP.items():
        text = text.replace(k, v)
    return text

def people_friendly_tamil(text):
    return text
