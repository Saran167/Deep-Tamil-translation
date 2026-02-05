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
import re

st.set_page_config(page_title="Tamil OCR Translator", page_icon="🪔", layout="wide")
st.title("🪔 Intelligent Tamil OCR Translation System")

# ---------------- IMAGE PREPROCESS ----------------
def preprocess_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )
    return thresh

# ---------------- OCR ----------------
def extract_text(image):
    processed = preprocess_image(image)
    return pytesseract.image_to_string(processed, lang="tam+eng")

# ---------------- OCR CORRECTION ----------------
def ocr_post_correction(text):
    char_map = {
        " ன்": "ன்",
        " ல்": "ல்",
        " ள்": "ள்",
        " ந்": "ன்",
        "ருு": "ரு",
        "ாா": "ா",
        "  ": " "
    }

    for k, v in char_map.items():
        text = text.replace(k, v)

    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 2]
    return " ".join(lines)

# ---------------- SANSKRIT DETECTION ----------------
def detect_sanskrit_words(text):
    sanskrit_roots = ["தர்ம", "கர்ம", "யோக", "பூஜ", "விதி", "ஸ்வ"]
    found = []

    for root in sanskrit_roots:
        if root in text:
            found.append(root)

    return found

# ---------------- TRANSLATION ----------------
def translate_to_tamil(text):
    return GoogleTranslator(source="auto", target="ta").translate(text)

# ---------------- VOICE ----------------
def tamil_voice(text):
    tts = gTTS(text=text, lang="ta")
    name = f"{uuid.uuid4().hex}.mp3"
    tts.save(name)
    return name

# ---------------- UI ----------------
tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "🖼️ Image"])
input_text = ""

with tab1:
    input_text = st.text_area("Enter text")
    if st.button("Translate"):
        st.session_state.text = input_text

with tab2:
    audio = st.file_uploader("Upload audio", type=["wav","mp3","m4a"])
    if audio and st.button("Convert"):
        r = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(audio.read())
            path = f.name
        with sr.AudioFile(path) as src:
            data = r.record(src)
            text = r.recognize_google(data)
        os.remove(path)
        st.session_state.text = text

with tab3:
    img_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image)
        if st.button("OCR + Translate"):
            raw = extract_text(image)
            corrected = ocr_post_correction(raw)
            st.session_state.text = corrected

# ---------------- OUTPUT ----------------
if "text" in st.session_state:
    st.subheader("📌 Processed Text")
    st.write(st.session_state.text)

    sanskrit_words = detect_sanskrit_words(st.session_state.text)
    if sanskrit_words:
        st.info(f"Sanskrit-origin words detected: {', '.join(sanskrit_words)}")

    tamil = translate_to_tamil(st.session_state.text)
    st.subheader("🇮🇳 Tamil Output")
    st.write(tamil)

    if st.button("🔊 Play Tamil Voice"):
        audio = tamil_voice(tamil)
        st.audio(audio)
        os.remove(audio)

st.caption("Research-ready OCR + Correction + Archaeology Support")

