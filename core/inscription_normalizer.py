import re

def normalize_stone_text(text):
    # remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # lower case
    text = text.lower()

    # fix compact words (demo logic)
    text = text.replace("urir", "ஊரிற்")
    text = text.replace("pugundaan", "புகுந்தான்")

    return text
