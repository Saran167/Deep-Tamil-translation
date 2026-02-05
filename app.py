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
import tempfile

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="People-Centric Tamil Language Interpretation System",
    page_icon="🪔",
    layout="wide"
)

# -------------------- BASIC STYLING --------------------
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

# -------------------- FUNCTIONS --------------------

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_to_tamil(text):
    return GoogleTranslator(source="auto", target="ta").translate(text)

# 🔑 CORE NOVELTY – Tamil Simplification
def simplify_tamil(text):
    simplification_map = {
        "இக்கல்வெட்டு": "இந்த கல்வெட்டு",
        "பிரதிபலிக்கிறது": "விளக்குகிறது",
        "முற்போக்கு": "முன்னேற்றம்",
        "செயற்கை நுண்ணறிவு": "மனிதனைப் போல சிந்திக்கும் கணினி தொழில்நுட்பம்",
        "பயன்படுத்தப்படுகிறது": "பயன்படுத்தப்படுகிறது (உபயோகிக்கப்படுகிறது)"
    }

    for hard, simple in simplification_map.items():
        text = text.replace(hard, simple)
    return text

def tamil_voice_output(text):
    tts = gTTS(text=text, lang="ta", slow=False)
    filename = f"tamil_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def process_audio_file(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        path = tmp.name

    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)

    os.unlink(path)
    return text

def create_pdf(original, tamil):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "People-Centric Tamil Interpretation System", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, f"Original Text:\n{original}")
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Simplified Tamil Output:\n{tamil}")

    name = f"tamil_output_{uuid.uuid4().hex[:6]}.pdf"
    pdf.output(name)
    return name

# -------------------- UI --------------------

st.markdown('<div class="main-title">🪔 People-Centric Tamil Language Interpretation System</div>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:white;'>Any Language → Simple, People-Understanding Tamil</p>",
    unsafe_allow_html=True
)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📥 Input Method</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "🖼️ Image"])
input_text = ""

with tab1:
    input_text = st.text_area("Enter text in any language", height=150)
    if st.button("Translate to Tamil"):
        st.session_state.text = input_text

with tab2:
    audio = st.file_uploader("Upload audio file", type=["wav", "mp3"])
    if audio and st.button("Convert Voice to Tamil"):
        st.session_state.text = process_audio_file(audio)

with tab3:
    image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if image and st.button("Extract & Translate"):
        st.session_state.text = extract_text_from_image(image)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- OUTPUT --------------------

if "text" in st.session_state:
    original = st.session_state.text
    raw_tamil = translate_to_tamil(original)
    simple_tamil = simplify_tamil(raw_tamil)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📤 Tamil Output</div>', unsafe_allow_html=True)

    st.markdown("### 🔹 Simplified Tamil (Final Output)")
    st.markdown(f"<div class='output-box'>{simple_tamil}</div>", unsafe_allow_html=True)

    if st.button("🔊 Listen Tamil"):
        audio = tamil_voice_output(simple_tamil)
        st.audio(audio)
        os.remove(audio)

    if st.button("📄 Download PDF"):
        pdf = create_pdf(original, simple_tamil)
        with open(pdf, "rb") as f:
            st.download_button("Download", f, file_name=pdf)
        os.remove(pdf)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("""
<hr>
<p style="text-align:center;color:white;">
Not a word-by-word translator.  
<br>Meaning-aware, people-centric Tamil interpretation system.
</p>
""", unsafe_allow_html=True)
