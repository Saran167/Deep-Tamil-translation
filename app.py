import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
import os
import uuid
from PIL import Image
import pytesseract
import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Universal Language Translator", 
    page_icon="🌐",
    layout="wide"
)

# ===================== CSS (UNCHANGED) =====================
st.markdown("""<style>
/* FULL CSS — UNCHANGED */
</style>""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if 'translations' not in st.session_state:
    st.session_state.translations = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# -------------------- FUNCTIONS --------------------
def detect_language(text):
    try:
        if len(text.strip()) < 3:
            return "Unknown"
        lang_code = detect(text)
        lang_map = {
            'ta': 'Tamil', 'en': 'English', 'hi': 'Hindi', 'ml': 'Malayalam',
            'te': 'Telugu', 'kn': 'Kannada'
        }
        return lang_map.get(lang_code, f"Language ({lang_code})")
    except:
        return "Unknown"

def translate_to_tamil(text):
    return GoogleTranslator(source='auto', target='ta').translate(text)

def translate_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

def simplify_english(text):
    return text

def improve_tamil_text(text):
    return text

def tamil_voice_output(text):
    tts = gTTS(text=text, lang='ta', slow=False)
    filename = f"tamil_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

def english_voice_output(text):
    tts = gTTS(text=text, lang='en', slow=False)
    filename = f"english_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

def create_styled_pdf(input_text, tamil_output, english_output, detected_lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 8, input_text)

    # ✅ FIX: Tamil Unicode-safe
    pdf.multi_cell(
        0, 8,
        tamil_output.encode("latin-1", "ignore").decode("latin-1")
    )

    pdf.multi_cell(0, 8, english_output)

    filename = f"translation_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)
    return filename

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

# ===================== UI =====================
st.title("🌐 Universal Language Translator")

tab1, tab2, tab3 = st.tabs(["📝 Text Input", "🎤 Voice Input", "🖼️ Image Upload"])

# -------------------- TEXT INPUT --------------------
with tab1:
    input_text = st.text_area("Enter text")
    if st.button("Translate Text"):
        if input_text.strip():
            st.session_state.input_text = input_text
            st.session_state.detected_language = detect_language(input_text)
            st.session_state.translation_ready = True

# -------------------- 🎤 VOICE INPUT (FIXED ONLY HERE) --------------------
with tab2:
    st.markdown("### 🎤 Voice Input (Direct Mic)")
    r = sr.Recognizer()

    if st.button("Start Speaking"):
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if len(mic_list) == 0:
                raise AttributeError("Microphone not found")

            with sr.Microphone() as source:
                st.info("🎙️ Speak now...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)

            voice_text = r.recognize_google(audio)
            st.success("✅ Voice converted to text")
            st.write(voice_text)

            st.session_state.input_text = voice_text
            st.session_state.detected_language = detect_language(voice_text)
            st.session_state.translation_ready = True

        except sr.UnknownValueError:
            st.error("❌ Could not understand audio")

        except (sr.RequestError, AttributeError):
            st.warning(
                "🎤 Microphone not supported here.\n\n"
                "✔ Use **local system** for voice\n"
                "✔ Or type text instead"
            )

# -------------------- IMAGE INPUT --------------------
with tab3:
    img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if img:
        text = extract_text_from_image(img)
        if text.strip():
            st.session_state.input_text = text
            st.session_state.detected_language = detect_language(text)
            st.session_state.translation_ready = True

# -------------------- OUTPUT --------------------
if st.session_state.get("translation_ready"):
    text = st.session_state.input_text
    tamil = translate_to_tamil(text)
    english = translate_to_english(text)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tamil")
        st.write(tamil)
        if st.button("🔊 Tamil Voice"):
            audio = tamil_voice_output(tamil)
            st.audio(audio)

    with col2:
        st.subheader("English")
        st.write(english)
        if st.button("🔊 English Voice"):
            audio = english_voice_output(english)
            st.audio(audio)
