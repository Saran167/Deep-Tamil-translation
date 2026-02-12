import json

def load_dictionary():
    try:
        with open("data/ancient_dictionary.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

dictionary = load_dictionary()

def convert_ancient_text(text):
    words = text.split()
    converted = []

    for word in words:
        converted.append(dictionary.get(word, word))

    return " ".join(converted)



