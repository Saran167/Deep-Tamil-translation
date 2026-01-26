import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
from PIL import Image
import pytesseract
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Deep Tamil Translator",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- FUNCTIONS ----------------
def translate_text(text, target):
    translator = GoogleTranslator(source="auto", target=target)
    return translator.translate(text)

def improve_tamil(text):
    rules = {
        "நான் இருக்கிறேன்": "நான் உள்ளேன்",
        "எனக்கு தெரியும்": "எனக்குத் தெரியும்",
        "மிகவும் நல்லது": "மிகச் சிறந்தது",
        "நீங்கள் எப்படி இருக்கிறீர்கள்": "நீங்கள் எப்படி உள்ளீர்கள்",
        "நான் செய்ய வேண்டும்": "நான் செய்ய வேண்டும் என்று நினைக்கிறேன்"
    }
    for k, v in rules.items():
        text = text.replace(k, v)
    return text

def simple_english(text):
    # Rewriting into simpler English
    return GoogleTranslator(source="auto", target="en").translate(text)

def text_to_voice(text, lang):
    tts = gTTS(text=text, lang=lang)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(file.name)
    return file.name

def create_pdf(input_text, output_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, "INPUT:\n" + input_text + "\n\nOUTPUT:\n" + output_text)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)
    return file.name

def image_to_text(img):
    return pytesseract.image_to_string(img)

# ---------------- UI ----------------
st.title("🌍 Any Language → Tamil / Simple English")
st.markdown("**Spoken Tamil focused translation for common people**")

input_mode = st.radio(
    "Choose Input Type",
    ["Text", "Voice", "Image"],
    horizontal=True
)

input_text = ""

# ---------------- TEXT INPUT ----------------
if input_mode == "Text":
    input_text = st.text_area(
        "✍️ Enter text in any language",
        height=200
    )

# ---------------- VOICE INPUT (DIRECT MIC – WORKING) ----------------
elif input_mode == "Voice":
    st.info("🎙️ Click record and speak")
    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes.getbuffer())
            audio_path = f.name

        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            input_text = r.recognize_google(audio)

        st.success("Voice converted to text")
        st.write(input_text)

# ---------------- IMAGE INPUT ----------------
elif input_mode == "Image":
    img_file = st.file_uploader(
        "🖼️ Upload image",
        type=["png", "jpg", "jpeg"]
    )
    if img_file:
        img = Image.open(img_file)
        input_text = image_to_text(img)
        st.success("Image converted to text")
        st.write(input_text)

# ---------------- OUTPUT PROCESS ----------------
if input_text:
    detected_lang = detect(input_text)
    st.info(f"Detected language: **{detected_lang.upper()}**")

    output_language = st.selectbox(
        "Select Output Language",
        ["Tamil", "English"]
    )

    if st.button("🚀 Translate"):
        if output_language == "Tamil":
            output_text = translate_text(input_text, "ta")
            output_text = improve_tamil(output_text)
            voice_lang = "ta"
        else:
            output_text = simple_english(input_text)
            voice_lang = "en"

        st.subheader("✅ Output")
        st.success(output_text)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔊 Voice Output"):
                audio_file = text_to_voice(output_text, voice_lang)
                st.audio(audio_file)
                st.download_button(
                    "Download Voice",
                    open(audio_file, "rb"),
                    "output_voice.mp3"
                )

        with col2:
            if st.button("📄 Download PDF"):
                pdf_file = create_pdf(input_text, output_text)
                st.download_button(
                    "Download PDF",
                    open(pdf_file, "rb"),
                    "translation.pdf"
                )

        st.markdown("### 👍 Feedback")
        st.button("Helpful")
        st.button("Not Helpful")
