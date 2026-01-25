import streamlit as st
from transformers import pipeline
import speech_recognition as sr
from gtts import gTTS
from PIL import Image
import pytesseract
from fpdf import FPDF
import tempfile
import os
import langdetect

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Tamil–English Translator",
    page_icon="🌈",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #fbc2eb, #a6c1ee);
}
.main {
    background-color: #ffffffcc;
    padding: 20px;
    border-radius: 20px;
}
h1 {
    color: #4a148c;
}
.stButton>button {
    background-color: #7b1fa2;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌈 Smart Spoken Tamil & Simple English Translator")
st.caption("Any Language ➜ Natural Tamil | Simple English")

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    translator = pipeline("translation", model="facebook/m2m100_418M")
    return translator

translator = load_models()

# ---------------- SPOKEN TAMIL RULES ----------------
def spoken_tamil(text):
    rules = {
        "நான்": "நா",
        "உங்களை": "உங்க",
        "உங்களுக்கு": "உங்க",
        "அழைப்பேன்": "கால் பண்ணுறேன்",
        "தகவல்": "விஷயம்",
        "அனுப்புவேன்": "அனுப்பிடுறேன்",
        "செல்லவும்": "போங்க",
        "இருக்கிறது": "இருக்கு",
        "உடனடியாக": "உடனே",
        "நாளை": "நாளைக்கு"
    }
    for k, v in rules.items():
        text = text.replace(k, v)
    return text

# ---------------- SIMPLE ENGLISH REWRITE ----------------
def simple_english(text):
    replacements = {
        "kindly": "please",
        "ensure": "make sure",
        "prior to": "before",
        "assist": "help",
        "purchase": "buy",
        "utilize": "use",
        "commence": "start",
        "terminate": "end"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# ---------------- TRANSLATION ----------------
def translate_text(text, target_lang):
    if target_lang == "English":
        translated = translator(text, src_lang="auto", tgt_lang="en")[0]["translation_text"]
        return simple_english(translated)
    else:
        translated = translator(text, src_lang="auto", tgt_lang="ta")[0]["translation_text"]
        return spoken_tamil(translated)

# ---------------- SPEECH TO TEXT ----------------
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

# ---------------- IMAGE TO TEXT ----------------
def image_to_text(img):
    return pytesseract.image_to_string(img)

# ---------------- PDF GENERATOR ----------------
def generate_pdf(input_text, output_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 8, "INPUT:\n" + input_text)
    pdf.ln(5)
    pdf.multi_cell(0, 8, "OUTPUT:\n" + output_text)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)
    return file.name

# ---------------- UI SECTIONS ----------------
st.subheader("📥 Choose Input Type")
input_type = st.radio("", ["📝 Text", "🎙️ Voice", "🖼️ Image"], horizontal=True)

st.subheader("🌐 Choose Output Language")
output_lang = st.radio("", ["Tamil", "English"], horizontal=True)

input_text = ""

# -------- TEXT INPUT --------
if input_type == "📝 Text":
    input_text = st.text_area("✍️ Enter text in any language")

# -------- VOICE INPUT --------
elif input_type == "🎙️ Voice":
    if st.button("🎤 Record Voice"):
        input_text = speech_to_text()
        st.success("Recognized Text:")
        st.write(input_text)

# -------- IMAGE INPUT --------
elif input_type == "🖼️ Image":
    img = st.file_uploader("📷 Upload Image", type=["png", "jpg", "jpeg"])
    if img:
        image = Image.open(img)
        st.image(image, width=300)
        input_text = image_to_text(image)

# ---------------- PROCESS ----------------
if st.button("✨ Convert"):
    if input_text.strip() == "":
        st.warning("Please provide input")
    else:
        output_text = translate_text(input_text, output_lang)

        st.subheader("📤 Output")
        st.success(output_text)

        # ----- AUDIO OUTPUT -----
        tts = gTTS(output_text, lang="ta" if output_lang == "Tamil" else "en")
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio_file.name)
        st.audio(audio_file.name)

        # ----- PDF DOWNLOAD -----
        pdf_path = generate_pdf(input_text, output_text)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF", f, file_name="translation.pdf")

        # ----- VOICE DOWNLOAD -----
        with open(audio_file.name, "rb") as f:
            st.download_button("🔊 Download Voice Output", f, file_name="output.mp3")
