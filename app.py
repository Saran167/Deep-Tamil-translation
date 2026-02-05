import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import os
import uuid
from PIL import Image
import pytesseract
import tempfile

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="People-Centric Tamil Language Interpretation System",
    page_icon="🪔",
    layout="wide"
)

# -------------------- STYLING --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.main-title {
    text-align: center;
    color: white;
    font-size: 2.6rem;
    font-weight: bold;
    padding: 20px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}
.section-header {
    font-size: 1.6rem;
    font-weight: bold;
    color: #764ba2;
}
.output-box {
    font-size: 18px;
    line-height: 1.8;
    background: #fff5f5;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- CORE FUNCTIONS --------------------

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_to_tamil(text):
    return GoogleTranslator(source="auto", target="ta").translate(text)

# 🔹 People-centric Tamil simplification
def simplify_tamil(text):
    simplification_map = {
        "இக்கல்வெட்டு": "இந்த கல்வெட்டு",
        "பிரதிபலிக்கிறது": "விளக்குகிறது",
        "முற்போக்கு": "முன்னேற்றம்",
        "பயன்படுத்தப்படுகிறது": "உபயோகிக்கப்படுகிறது",
        "செயற்கை நுண்ணறிவு": "மனிதனைப் போல சிந்திக்கும் கணினி தொழில்நுட்பம்"
    }
    for hard, simple in simplification_map.items():
        text = text.replace(hard, simple)
    return text

# 🔊 Tamil voice
def tamil_voice_output(text):
    tts = gTTS(text=text, lang="ta", slow=False)
    filename = f"tamil_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

# 🧠 OCR ERROR CORRECTION (NEW INTELLIGENCE)
def correct_tamil_ocr_errors(text):
    corrections = {
        " ல ": " ள ",
        " ர ": " ற ",
        " ன ": " ந ",
        " ட ": " ண ",
        " ா": "அ",
        " ி": "இ",
        " ு": "உ",
        " ெ": "எ",
        " ொ": "ஒ"
    }

    for wrong, right in corrections.items():
        text = text.replace(wrong, right)

    return text

# 🖼️ Image OCR + correction
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    raw_text = pytesseract.image_to_string(image, lang="tam")
    corrected_text = correct_tamil_ocr_errors(raw_text)
    return corrected_text

# 🎤 Voice input
def process_audio_file(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        path = tmp.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)

    os.unlink(path)
    return text

# -------------------- UI --------------------

st.markdown('<div class="main-title">🪔 People-Centric Tamil Language Interpretation System</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:white;'>Any Language → Simple, People-Understanding Tamil</p>",
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📥 Input Method</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "🖼️ Image"])

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---- TEXT ----
with tab1:
    txt = st.text_area("Enter text in any language", height=150)
    if st.button("Translate to Tamil", key="text_btn"):
        st.session_state.input_text = txt

# ---- VOICE ----
with tab2:
    audio = st.file_uploader("Upload audio file", type=["wav", "mp3"])
    if audio and st.button("Convert Voice to Tamil", key="voice_btn"):
        st.session_state.input_text = process_audio_file(audio)

# ---- IMAGE ----
with tab3:
    image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if image and st.button("Extract & Translate", key="img_btn"):
        st.session_state.input_text = extract_text_from_image(image)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- OUTPUT --------------------

if st.session_state.input_text.strip():
    original_text = st.session_state.input_text
    tamil_text = translate_to_tamil(original_text)
    simplified_tamil = simplify_tamil(tamil_text)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 Tamil Output</div>', unsafe_allow_html=True)

    st.markdown("### 🔹 Simplified Tamil Output")
    st.markdown(f"<div class='output-box'>{simplified_tamil}</div>", unsafe_allow_html=True)

    if st.button("🔊 Listen Tamil"):
        audio_file = tamil_voice_output(simplified_tamil)
        st.audio(audio_file)
        os.remove(audio_file)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("""
<hr>
<p style="text-align:center;color:white;">
<b>Not a word-by-word translator.</b><br>
Meaning-aware, people-centric Tamil interpretation system.<br>
Enhanced with OCR correction for archaeological & real-world images.
</p>
""", unsafe_allow_html=True)

