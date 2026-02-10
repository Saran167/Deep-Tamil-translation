import requests

LIBRE_URL = "https://libretranslate.de/translate"

def translate_to_tamil(text):
    try:
        payload = {
            "q": text,
            "source": "auto",
            "target": "ta",
            "format": "text"
        }

        response = requests.post(LIBRE_URL, data=payload, timeout=10)

        if response.status_code == 200:
            return response.json().get("translatedText", "")
        else:
            return ""

    except Exception:
        return ""
