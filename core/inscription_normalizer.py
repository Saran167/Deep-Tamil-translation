import re

def normalize_stone_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    return text

