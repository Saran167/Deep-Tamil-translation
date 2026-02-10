def simplify_modern_text(text: str) -> dict:
    """
    Convert modern / mixed language text into simple Tamil.
    """

    text_lower = text.strip().lower()

    simple_dictionary = {
        "how are you": {
            "simple": "நீ எப்படி இருக்கிறாய்",
            "people": "நீ நல்லா இருக்கியா"
        },
        "what is your name": {
            "simple": "உன் பெயர் என்ன",
            "people": "உன் பேர் என்ன"
        },
        "thank you": {
            "simple": "நன்றி",
            "people": "ரொம்ப நன்றி"
        }
    }

    if text_lower in simple_dictionary:
        return {
            "simple_tamil": simple_dictionary[text_lower]["simple"],
            "people_tamil": simple_dictionary[text_lower]["people"]
        }

    return {
        "simple_tamil": "இந்த வாக்கியம் தற்போது ஆதரிக்கப்படவில்லை",
        "people_tamil": "இந்த வாக்கியத்தை எளிமையாக மாற்ற முடியவில்லை"
    }
