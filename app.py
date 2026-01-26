import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
from PIL import Image
import pytesseract
import os
import tempfile

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Multilingual → Tamil & English", layout="wide")
translator = Translator()

# ---------------- FUNCTIONS ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def chunk_text(text, max_len=4500):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

def translate_text(text, target_lang):
    chunks = chunk_text(text)
    final_text = ""
    for chunk in chunks:
        translated = translator.translate(chunk, dest=target_lang)
        final_text += translated.text + " "
    return final_text.strip()

def improve_tamil(text):
    replacements = {
        "நான் இருக்கிறேன்": "நான் உள்ளேன்",
        "எனக்கு தெரியும்": "எனக்குத் தெரியும்",
        "மிகவும் நல்லது": "மிகச் சிறந்தது"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def simple_english(text):
    simplified = translator.translate(text, dest="en").text
    return simplified

def text_to_voice(text, lang):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)
    return file.name

def image_to_text(image):
    return pytesseract.image_to_string(image)

# ---------------- UI ----------------
st.title("🌐 Multilingual Input → Tamil & English Output")

st.markdown("### 🔹 Step 1: Choose Input Method")

input_mode = st.radio("", ["Text Input", "Voice Input", "Image Upload"])

input_text = ""

# -------- TEXT INPUT --------
if input_mode == "Text Input":
    input_text = st.text_area("📝 Enter text (Any Language)", height=200)

# -------- VOICE INPUT --------
elif input_mode == "Voice Input":
    st.info("🎤 Record your voice and upload audio file")
    audio_file = st.file_uploader("Upload Audio (.wav)", type=["wav"])
    if audio_file:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        input_text = r.recognize_google(audio)
        st.success("Voice converted to text")
        st.write(input_text)

# -------- IMAGE INPUT --------
elif input_mode == "Image Upload":
    image_file = st.file_uploader("📷 Upload Image", type=["png", "jpg", "jpeg"])
    if image_file:
        img = Image.open(image_file)
        input_text = image_to_text(img)
        st.success("Image converted to text")
        st.write(input_text)

# ---------------- PROCESS ----------------
if input_text:
    detected_lang = detect_language(input_text)
    st.markdown(f"### 🔍 Detected Language: **{detected_lang.upper()}**")

    st.markdown("### 🔹 Step 2: Output Language")
    output_lang = st.selectbox("", ["Tamil", "English"])

    if st.button("🔄 Translate"):
        if output_lang == "Tamil":
            translated = translate_text(input_text, "ta")
            translated = improve_tamil(translated)
            lang_code = "ta"
        else:
            translated = simple_english(input_text)
            lang_code = "en"

        st.markdown("## ✅ Output Text")
        st.success(translated)

        # -------- OUTPUT OPTIONS --------
        st.markdown("### 🔹 Step 3: Output Options")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔊 Generate Voice"):
                audio_path = text_to_voice(translated, lang_code)
                st.audio(audio_path)
                st.download_button("⬇ Download Voice", open(audio_path, "rb"), file_name="output.mp3")

        with col2:
            if st.button("📄 Generate PDF"):
                pdf_path = create_pdf(translated)
                st.download_button("⬇ Download PDF", open(pdf_path, "rb"), file_name="output.pdf")

        # -------- FEEDBACK --------
        st.markdown("### 🙏 Feedback")
        fb1, fb2 = st.columns(2)
        fb1.button("👍 Helpful")
        fb2.button("👎 Not Helpful")
