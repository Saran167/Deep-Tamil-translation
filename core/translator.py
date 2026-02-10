from deep_translator import GoogleTranslator

def translate_to_tamil(text):
    try:
        translated = GoogleTranslator(
            source="auto",
            target="ta"
        ).translate(text)
        return translated
    except Exception:
        return ""
