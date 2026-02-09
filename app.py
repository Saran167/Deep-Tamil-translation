import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Simple Tamil Translator",
    page_icon="🧠",
    layout="wide"
)

# -------------------- FUNCTIONS --------------------

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_to_tamil(text):
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except:
        return "Translation failed"

def simplify_tamil(text):
    # Basic placeholder simplification
    replacements = {
        "மிகவும்": "ரொம்ப",
        "தேவையான": "வேண்டிய",
        "பயன்படுத்தப்படுகிறது": "பயன்படுகிறது",
        "உள்ளது": "இருக்கு"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def ocr_image(image):
    return pytesseract.image_to_string(image, lang="tam+eng")

def ocr_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

# -------------------- HEADER --------------------
st.title("🧠 Dual-Phase Intelligent Tamil Translation System")
st.subheader("Phase-1: Any Language → Simple, People-Friendly Tamil")

st.markdown(
    "This phase converts **any language** into **easy modern Tamil** that common people can understand."
)

st.divider()

# -------------------- INPUT TYPE --------------------
input_type = st.radio(
    "📥 Select Input Type",
    ["Text", "Voice", "Image", "PDF"],
    horizontal=True
)

input_text = ""

# -------------------- INPUT UI --------------------
if input_type == "Text":
    input_text = st.text_area(
        "✍️ Enter text in any language",
        height=200
    )

elif input_type == "Voice":
    if st.button("🎙️ Start Voice Input"):
        input_text = voice_to_text()
        st.success("Voice captured successfully!")
        st.text_area("Recognized Text", input_text, height=150)

elif input_type == "Image":
    image_file = st.file_uploader("📷 Upload Image", type=["jpg", "png", "jpeg"])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        input_text = ocr_image(image)
        st.text_area("Extracted Text", input_text, height=150)

elif input_type == "PDF":
    pdf_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
    if pdf_file:
        input_text = ocr_pdf(pdf_file)
        st.text_area("Extracted Text", input_text, height=150)

st.divider()

# -------------------- PROCESS --------------------
if st.button("🔄 Convert to Simple Tamil", type="primary"):

    if not input_text.strip():
        st.warning("Please provide input!")
    else:
        with st.spinner("Processing..."):

            detected_lang = detect_language(input_text)
            tamil_text = translate_to_tamil(input_text)
            simple_tamil = simplify_tamil(tamil_text)

        st.success("✅ Conversion Completed")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📄 Original Text")
            st.markdown(f"**Detected Language:** `{detected_lang}`")
            st.text_area("Input", input_text, height=220)

        with col2:
            st.markdown("### ✅ Simple Tamil Output")
            st.text_area("Simplified Tamil", simple_tamil, height=220)

        st.download_button(
            "⬇️ Download Output",
            simple_tamil,
            file_name="simple_tamil_translation.txt"
        )

# -------------------- SIDEBAR --------------------
st.sidebar.title("ℹ️ Phase-1 Info")
st.sidebar.markdown(
    """
    **Features**
    - Auto language detection
    - Translation to Tamil
    - Simple spoken Tamil
    - Text, Voice, Image & PDF input
    """
)
st.sidebar.markdown("---")
st.sidebar.markdown("🎓 Useful for common people & beginners")


