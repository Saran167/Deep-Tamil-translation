import streamlit as st
import numpy as np
import cv2
from PIL import Image
import pytesseract
from langdetect import detect
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Dual-Phase Tamil Translation System",
    layout="wide"
)

st.title("🪔 Dual-Phase Tamil Translation System")
st.caption("Simple Tamil for Users | Ancient Tamil for Archaeologists")

# -------------------------------------------------
# UTILITIES
# -------------------------------------------------

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def safe_ocr(image):
    try:
        text = pytesseract.image_to_string(
            image, lang="tam+eng", config="--psm 6"
        )
        return text.strip()
    except:
        return ""


def ocr_quality(text):
    length = len(text.strip())
    if length == 0:
        return "FAILED"
    elif length < 30:
        return "POOR"
    elif length < 100:
        return "AVERAGE"
    else:
        return "GOOD"


def clean_ancient_ocr(text):
    words = text.split()
    cleaned = []

    for w in words:
        if len(w) > 2 and not any(ch.isdigit() for ch in w):
            cleaned.append(w)

    return cleaned


def ancient_to_modern_tamil(fragments):
    # Rule-based interpretation (research-friendly)
    interpreted = []
    for word in fragments:
        interpreted.append(word)  # placeholder for linguistic rules

    return " ".join(interpreted)


def simple_tamil_translate(text):
    try:
        return GoogleTranslator(source="auto", target="ta").translate(text)
    except:
        return "Translation failed."


def tamil_voice(text):
    tts = gTTS(text=text, lang="ta")
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    return temp.name


# -------------------------------------------------
# UI – MODE SELECTION
# -------------------------------------------------

mode = st.radio(
    "Choose Translation Mode",
    ["🧑‍🤝‍🧑 Simple Tamil (Common Users)",
     "🏺 Ancient Tamil (Archaeology)"]
)

# =================================================
# PHASE 1 – SIMPLE TAMIL
# =================================================
if mode == "🧑‍🤝‍🧑 Simple Tamil (Common Users)":

    st.subheader("🔤 Enter Any Language Text")

    input_text = st.text_area("Enter text here")

    if st.button("Convert to Simple Tamil"):
        if input_text.strip() != "":
            translated = simple_tamil_translate(input_text)
            st.success("✅ Simple Tamil Output")
            st.write(translated)

            audio = tamil_voice(translated)
            st.audio(audio)
        else:
            st.warning("Please enter text.")


# =================================================
# PHASE 2 – ANCIENT TAMIL
# =================================================
if mode == "🏺 Ancient Tamil (Archaeology)":

    st.subheader("📜 Upload Ancient Tamil Image")

    uploaded = st.file_uploader(
        "Upload Inscription / Manuscript Image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded)
        img_np = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        processed = preprocess_image(img_np)
        raw_text = safe_ocr(processed)

        quality = ocr_quality(raw_text)

        st.markdown("### 🔍 OCR Analysis")
        st.write("OCR Quality:", quality)
        st.text_area("Raw OCR Text", raw_text, height=120)

        if quality != "FAILED":
            cleaned = clean_ancient_ocr(raw_text)

            st.markdown("### 🧹 Corrected Ancient Tamil Fragments")
            st.write(cleaned)

            modern_tamil = ancient_to_modern_tamil(cleaned)

            st.markdown("### 🟢 Modern Tamil Interpretation")
            st.write(modern_tamil)

            audio = tamil_voice(modern_tamil)
            st.audio(audio)
        else:
            st.error(
                "OCR failed. Image quality too low or script too complex."
            )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Academic Prototype | Dual-Phase NLP + OCR + Tamil Linguistics"
)


