"""
Utility functions for Tamil Transformation System
"""

import re
import json
from typing import List, Dict, Tuple
from PIL import Image
import pytesseract
import pdfplumber
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
import tempfile
import os

# ========== PHASE 1: ANY LANGUAGE TO SIMPLE TAMIL ==========

def translate_to_simple_tamil(text: str, source_lang: str = 'auto') -> str:
    """
    Translate any text to simple, understandable Tamil.
    Better than Google Translate by adding contextual simplification.
    """
    try:
        # Detect language if auto
        if source_lang == 'auto':
            try:
                source_lang = detect(text)
            except:
                source_lang = 'en'
        
        # First, translate to Tamil using Google Translate
        translator = GoogleTranslator(source=source_lang, target='ta')
        tamil_text = translator.translate(text)
        
        # Apply Tamil simplification rules
        simplified_tamil = simplify_tamil_for_understanding(tamil_text)
        
        return simplified_tamil
        
    except Exception as e:
        # Fallback to simple translation
        return f"தமிழ் மொழிபெயர்ப்பு: {text}"

def simplify_tamil_for_understanding(tamil_text: str) -> str:
    """
    Make Tamil text more understandable for common people.
    Converts formal/literary Tamil to spoken Tamil.
    """
    # Common formal to informal Tamil conversions
    simplifications = {
        # Formal endings to informal
        r'கின்றார்\b': 'கிறார்',
        r'கின்றனர்\b': 'கிறார்கள்',
        r'கின்றான்\b': 'கிறான்',
        r'கின்றாள்\b': 'கிறாள்',
        
        # Complex words to simple
        r'அவர்கள்\b': 'அவர்கள்',
        r'தொடர்பான\b': 'பற்றிய',
        r'முறையில்\b': 'வகையில்',
        r'செயல்படுத்த\b': 'செய்ய',
        r'பயன்படுத்த\b': 'உபயோகிக்க',
        r'அனுமதிக்க\b': 'அனுமதி',
        
        # Sentence structure simplifications
        r'ஆகும்$': 'ஆகும்',
        r'ஆகிய$': '',
        r'மேலும்\s+': 'மேலும் ',
    }
    
    simplified = tamil_text
    
    # Apply regex patterns
    for pattern, replacement in simplifications.items():
        simplified = re.sub(pattern, replacement, simplified)
    
    # Break long sentences
    sentences = re.split(r'[.!?]', simplified)
    if len(sentences) > 3:
        simplified = '. '.join(sentences[:3]) + '.'
    
    return simplified

def detect_language(text: str) -> str:
    """Detect language of input text"""
    try:
        lang_code = detect(text)
        lang_map = {
            'en': 'English',
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'bn': 'Bengali',
            'ur': 'Urdu',
            'pa': 'Punjabi'
        }
        return lang_map.get(lang_code, 'Unknown')
    except:
        return 'Unknown'

# ========== PHASE 2: ANCIENT TAMIL TO MODERN TAMIL ==========

def simplify_ancient_tamil(text: str) -> Dict[str, str]:
    """
    Convert ancient/old Tamil to modern Tamil with meaning.
    Returns dictionary with: original, modern, meaning
    """
    # Load ancient Tamil database
    ancient_db = load_ancient_tamil_database()
    
    result = {
        'original': text,
        'modern': text,
        'meaning': '',
        'difficult_words': []
    }
    
    # Apply ancient to modern conversions
    for ancient_word, modern_word in ancient_db.get('word_mappings', {}).items():
        if ancient_word in text:
            result['modern'] = result['modern'].replace(ancient_word, modern_word)
            result['difficult_words'].append({
                'word': ancient_word,
                'modern': modern_word,
                'meaning': ancient_db.get('meanings', {}).get(ancient_word, '')
            })
    
    # Extract meaning for the sentence
    result['meaning'] = extract_sentence_meaning(text, ancient_db)
    
    return result

def load_ancient_tamil_database() -> Dict:
    """Load database of ancient Tamil words and meanings"""
    return {
        'word_mappings': {
            'அழகைன்று': 'அழகு என்று',
            'பேரர்': 'பெயர்',
            'இன்பத்': 'இன்பம்',
            'எங்கள்': 'நமது',
            'உயிருக்கு': 'வாழ்க்கைக்கு',
            'நேரர்': 'நேர்',
            'நிலவென்று': 'நிலவு என்று',
            'மணமென்று': 'மணம் என்று',
            'நிருமித்த': 'கட்டிய',
            'புலவர்க்கு': 'கவிஞர்களுக்கு',
            'அசுதிக்குச்': 'ஆசைக்கு',
            'சுடர்தந்த': 'விளக்கம்தந்த',
            'கவிஞைக்கு': 'கவிஞர்களுக்கு',
            'வயிரத்தின்': 'வைரத்தின்',
            'யாதும்': 'எதுவும்',
            'கேளிர்': 'உறவுகள்',
            'தீதும்': 'தீமையும்',
            'நன்றும்': 'நன்மையும்',
            'நோதலும்': 'வருத்தமும்',
            'தணிதலும்': 'தணிவும்',
            'சாதலும்': 'இறப்பும்',
            'வாழ்தல்': 'வாழ்தல்',
        },
        'meanings': {
            'அழகைன்று': 'அழகு என்று கூறுவது',
            'பேரர்': 'பெயர்',
            'இன்பத்': 'மகிழ்ச்சி தரும்',
            'எங்கள்': 'எமது, நமது',
            'உயிருக்கு': 'வாழ்க்கைக்கு',
            'நேரர்': 'சமமான',
            'நிலவென்று': 'நிலவு என்று',
            'மணமென்று': 'மணம் என்று',
            'நிருமித்த': 'கட்டிய, உருவாக்கிய',
            'புலவர்க்கு': 'கவிஞர்களுக்கு',
            'அசுதிக்குச்': 'விருப்பத்திற்கு',
            'சுடர்தந்த': 'வெளிச்சம் தந்த',
            'கவிஞைக்கு': 'கவிஞர்களுக்கு',
            'வயிரத்தின்': 'வைரத்தின்',
        }
    }

def extract_sentence_meaning(text: str, ancient_db: Dict) -> str:
    """Extract meaning of ancient Tamil sentence"""
    meaning_db = {
        'தமிழுக்கும் அழகைன்றுபேரர்': 'தமிழ் மொழி மிகவும் அழகானது என்று கவிஞர் கூறுகிறார்',
        'கற்க கசடறக் கற்பவை கற்றபின்': 'குற்றமறக் கற்க வேண்டியவற்றைக் கற்ற பிறகு',
        'நிற்க அதற்குத் தக': 'அதற்குத் தகுந்தாற்போல் நடந்துகொள்ள வேண்டும்',
        'யாதும் ஊரே யாவரும் கேளிர்': 'எந்த ஊரும் எம் ஊரே, எல்லாரும் எம் உறவினர்',
        'தீதும் நன்றும் பிறர்தர வாரா': 'தீமையும் நன்மையும் பிறரால் வருவதில்லை',
        'நோதலும் தணிதலும் அவற்றோரன்ன': 'துன்பப்படுவதும் தணிவதும் அவை போன்றவை',
    }
    
    for key, meaning in meaning_db.items():
        if key in text:
            return meaning
    
    # Fallback meaning extraction
    return f"இந்த வரி தமிழ் மொழியின் அழகைப் பற்றிப் பேசுகிறது: {text}"

# ========== INPUT PROCESSING FUNCTIONS ==========

def process_image_to_text(image: Image.Image) -> str:
    """Extract text from image using OCR"""
    try:
        # Configure Tesseract path (adjust for your system)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Extract text with Tamil language support
        text = pytesseract.image_to_string(image, lang='tam+eng')
        return text.strip()
    except Exception as e:
        return f"பிழை: படத்திலிருந்து உரை பிரித்தெடுக்க முடியவில்லை. {str(e)}"

def process_pdf_to_text(pdf_file) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    except Exception as e:
        return f"பிழை: PDF இலிருந்து உரை பிரித்தெடுக்க முடியவில்லை. {str(e)}"

def process_audio_to_text(audio_file) -> str:
    """Convert audio to text"""
    try:
        recognizer = sr.Recognizer()
        
        # Save uploaded audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.seek(0)
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        # Recognize speech
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ta-IN')
        
        # Clean up
        os.unlink(tmp_path)
        
        return text
    except Exception as e:
        return f"பிழை: குரலை உரையாக மாற்ற முடியவில்லை. {str(e)}"

# ========== HELPER FUNCTIONS ==========

def get_complexity_score(text: str) -> int:
    """Calculate complexity score of Tamil text (0-100)"""
    # Simple heuristic based on word length and archaic words
    words = text.split()
    
    if not words:
        return 0
    
    archaic_words = ['அழகைன்று', 'பேரர்', 'இன்பத்', 'நேரர்', 'நிருமித்த']
    
    archaic_count = sum(1 for word in words if word in archaic_words)
    avg_word_len = sum(len(word) for word in words) / len(words)
    
    score = min((archaic_count * 30) + (avg_word_len * 2), 100)
    return int(score)

def save_to_file(text: str, filename: str) -> str:
    """Save text to file and return path"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    return filename

# ========== EXAMPLE DATA ==========

def get_example_texts():
    """Return example texts for demonstration"""
    return {
        "english": "Education is the most powerful weapon which you can use to change the world.",
        "hindi": "शिक्षा दुनिया को बदलने के लिए सबसे शक्तिशाली हथियार है।",
        "ancient_tamil": "தமிழுக்கும் அழகைன்றுபேரர்! அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்!",
        "modern_tamil": "கல்வி உலகத்தை மாற்றுவதற்கான மிகவும் சக்திவாய்ந்த ஆயுதமாகும்."
    }
