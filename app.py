import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from PIL import Image
import pytesseract
import tempfile
import os
import uuid
import cv2
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Tamil Intelligent Translator",
    page_icon="🪔",
    layout="wide"
)

st.title("🪔 Intelligent Tamil Translation System")
st.write("**Any Language → Simple, People-Friendly Tamil**")

# ---------------- FUNCTIONS ----------------

def preprocess_image(image):
    """Improve image quality for OCR"""
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )
    return thresh


def extract_text_from_image(image):
    processed = preprocess_image(image)
    text = pytesseract.image_to_string(processed, lang="tam+eng")
    return text


def ocr_correction(text):
    """Basic OCR correction for ALL images"""
    corrections = {
        "0": "o",
        "1": "l",
        "|": "l",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "—": "-",
        "_": " ",
        "  ": " "
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)

    lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 2]
    return " ".join(lines)


def translate_to_simple_tamil(text):
    tamil = GoogleTranslator(source="auto", target="ta").translate(text)
    return tamil


def tamil_voice(text):
    tts = gTTS(text=text, lang="ta")
    filename = f"tamil_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename


def speech_to_text(audio_file):
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    with sr.AudioFile(tmp_path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio)

    os.unlink(tmp_path)
    return text

# ---------------- INPUT UI ----------------

tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "🖼️ Image"])

input_text = ""

# -------- TEXT INPUT --------
with tab1:
    input_text = st.text_area("Enter text in any language", height=150)
    if st.button("Translate Text"):
        st.session_state.text = input_text

# -------- VOICE INPUT --------
with tab2:
    audio = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
    if audio and st.button("Convert Voice"):
        text = speech_to_text(audio)
        st.session_state.text = text
        st.success(f"Recognized Text: {text}")

# -------- IMAGE INPUT --------
with tab3:
    image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image")

        if st.button("Extract & Translate"):
            raw_text = extract_text_from_image(image)
            corrected_text = ocr_correction(raw_text)
            st.session_state.text = corrected_text
            st.success("OCR + Correction Applied")

# ---------------- OUTPUT ----------------

if "text" in st.session_state and st.session_state.text.strip():
    st.markdown("---")
    st.subheader("📌 Extracted / Input Text")
    st.write(st.session_state.text)

    tamil = translate_to_simple_tamil(st.session_state.text)

    st.subheader("🇮🇳 Tamil Output (People-Friendly)")
    st.write(tamil)

    if st.button("🔊 Play Tamil Voice"):
        audio_file = tamil_voice(tamil)
        st.audio(audio_file)
        os.remove(audio_file)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🔬 Research-Oriented Tamil Translation | OCR + Correction + Speech | Archaeology Ready")
