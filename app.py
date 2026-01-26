import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
from PIL import Image
import pytesseract
import tempfile

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Deep Tamil Translator", layout="wide")

# ---------------- FUNCTIONS ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def chunk_text(text, size=4500):
    return [text[i:i+size] for i in range(0, len(text), size)]

def translate_text(text, target):
    translator = GoogleTranslator(source="auto", target=target)
    output = ""
    for chunk in chunk_text(text):
        output += translator.translate(chunk) + " "
    return output.strip()

def improve_tamil(text):
    rules = {
        "நான் இருக்கிறேன்": "நான் உள்ளேன்",
        "எனக்கு தெரியும்": "எனக்குத் தெரியும்",
        "மிகவும் நல்லது": "மிகச் சிறந்தது",
        "நீங்கள் எப்படி இருக்கிறீர்கள்": "நீங்கள் எப்படி உள்ளீர்கள்"
    }
    for k, v in rules.items():
        text = text.replace(k, v)
    return text

def simple_english(text):
    simplified = GoogleTranslator(source="auto", target="en").translate(text)
    return simplified

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
st.title("🌐 Any Language → Tamil / Simple English")

input_mode = st.radio("Choose Input Type", ["Text", "Voice", "Image"])

input_text = ""

# TEXT INPUT
if input_mode == "Text":
    input_text = st.text_area("Enter text", height=200)

# VOICE INPUT
elif input_mode == "Voice":
    audio = st.file_uploader("Upload WAV audio", type=["wav"])
    if audio:
        r = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            input_text = r.recognize_google(r.record(source))
        st.success("Voice converted to text")
        st.write(input_text)

# IMAGE INPUT
elif input_mode == "Image":
    img_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        input_text = image_to_text(img)
        st.success("Image converted to text")
        st.write(input_text)

# PROCESS
if input_text:
    lang = detect_language(input_text)
    st.info(f"Detected language: {lang.upper()}")

    output_lang = st.selectbox("Select Output Language", ["Tamil", "English"])

    if st.button("Translate"):
        if output_lang == "Tamil":
            result = improve_tamil(translate_text(input_text, "ta"))
            lang_code = "ta"
        else:
            result = simple_english(input_text)
            lang_code = "en"

        st.subheader("Output")
        st.success(result)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔊 Voice Output"):
                audio_path = text_to_voice(result, lang_code)
                st.audio(audio_path)
                st.download_button("Download Voice", open(audio_path, "rb"), "output.mp3")

        with col2:
            if st.button("📄 Download PDF"):
                pdf_path = create_pdf(input_text, result)
                st.download_button("Download PDF", open(pdf_path, "rb"), "output.pdf")

        st.markdown("### Feedback")
        st.button("👍 Helpful")
        st.button("👎 Not Helpful")
