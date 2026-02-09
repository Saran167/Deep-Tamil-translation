import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from PIL import Image
import pytesseract
import pdfplumber
import speech_recognition as sr
from gtts import gTTS
import os
import uuid

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Context-Aware Tamil Interpretation System",
    layout="wide"
)

st.title("📘 Context-Aware Tamil Language Interpretation System")
st.caption("Student-friendly Tamil understanding for modern and classical content")

# ------------------ FUNCTIONS ------------------

def simple_tamil_rewrite(text):
    """
    Converts translated Tamil into simpler, student-friendly Tamil
    (rule-based simplification – lightweight & explainable)
    """
    replacements = {
        "வழங்கினார்": "கொடுத்தார்",
        "தானமாக": "இலவசமாக",
        "இந்நிலம்": "இந்த நிலம்",
        "கோயில்": "கோவில்",
        "அளிக்கப்பட்டது": "கொடுக்கப்பட்டது"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def translate_to_tamil(text):
    lang = detect(text)
    translated = GoogleTranslator(source=lang, target="ta").translate(text)
    simplified = simple_tamil_rewrite(translated)
    return simplified


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang="tam")
    return text.strip()


def extract_text_from_pdf(pdf_file):
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() or ""
    return extracted_text.strip()


def tamil_tts(text):
    file_name = f"tamil_{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang="ta")
    tts.save(file_name)
    return file_name


# ------------------ INPUT SECTIONS ------------------

option = st.sidebar.selectbox(
    "Choose Input Type",
    ["Text", "Voice", "Image", "PDF"]
)

final_text = ""

# -------- TEXT INPUT --------
if option == "Text":
    input_text = st.text_area("Enter text in ANY language")
    if st.button("Convert to Simple Tamil"):
        final_text = translate_to_tamil(input_text)

# -------- VOICE INPUT --------
elif option == "Voice":
    audio_file = st.file_uploader("Upload voice file (wav/mp3)", type=["wav", "mp3"])
    if audio_file:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            final_text = translate_to_tamil(text)
        except:
            st.error("Could not recognize audio")

# -------- IMAGE INPUT --------
elif option == "Image":
    image_file = st.file_uploader("Upload Tamil image (old / classical / textbook)", type=["jpg", "png", "jpeg"])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", width=400)
        extracted = extract_text_from_image(image)
        if extracted:
            final_text = translate_to_tamil(extracted)
        else:
            st.warning("Text not clear enough")

# -------- PDF INPUT --------
elif option == "PDF":
    pdf_file = st.file_uploader("Upload Tamil lesson / chapter PDF", type=["pdf"])
    if pdf_file:
        extracted = extract_text_from_pdf(pdf_file)
        if extracted:
            final_text = translate_to_tamil(extracted)
        else:
            st.warning("No readable text found")

# ------------------ OUTPUT ------------------

if final_text:
    st.subheader("✅ Student-Friendly Modern Tamil Output")
    st.write(final_text)

    audio_path = tamil_tts(final_text)
    st.audio(audio_path)

    st.info("✔ Output rewritten for easy student understanding (not literal translation)")


