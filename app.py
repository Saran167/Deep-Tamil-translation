import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Dual-Phase Tamil Translation System",
    page_icon="📘",
    layout="wide"
)

# ================= UTILITY FUNCTIONS =================

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_to_tamil(text):
    try:
        return GoogleTranslator(source="auto", target="ta").translate(text)
    except:
        return "❌ Translation failed"

def simplify_tamil(text):
    replacements = {
        "மிகவும்": "ரொம்ப",
        "தேவையான": "வேண்டிய",
        "பயன்படுத்தப்படுகிறது": "பயன்படுகிறது",
        "உள்ளது": "இருக்கு",
        "முடியும்": "செய்யலாம்"
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
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def audio_file_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

# ================= PHASE-2 DICTIONARY =================

ANCIENT_TAMIL_DICT = {
    "யாதும்": "எல்லாவும்",
    "ஊரே": "ஊர்",
    "யாவரும்": "எல்லோரும்",
    "கேளிர்": "உறவினர்கள்",
    "அறம்": "நல்ல செயல்",
    "போர்": "சண்டை",
    "புலவர்": "கவிஞர்",
    "மன்னன்": "அரசன்"
}

def ancient_to_modern_tamil(text):
    modern = text
    for ancient, modern_word in ANCIENT_TAMIL_DICT.items():
        modern = modern.replace(ancient, modern_word)
    return modern

def generate_meaning(modern_text):
    return f"இந்த வரியின் எளிய பொருள்: {modern_text}."

# ================= APP HEADER =================
st.title("📘 Dual-Phase Intelligent Tamil Translation & Learning System")
st.markdown(
    """
    **Phase-1:** Any Language → Simple Modern Tamil  
    **Phase-2:** Ancient / Old Tamil → Modern Tamil + Meaning
    """
)

st.divider()

# ================= TABS =================
tab1, tab2 = st.tabs([
    "Phase-1: Simple Tamil Translator",
    "Phase-2: Ancient Tamil Learning"
])

# ================= PHASE 1 =================
with tab1:
    st.subheader("🧠 Phase-1: Any Language → Simple Tamil")

    input_type = st.radio(
        "📥 Select Input Type",
        ["Text", "Voice (Audio Upload)", "Image", "PDF"],
        horizontal=True
    )

    input_text = ""

    if input_type == "Text":
        input_text = st.text_area("Enter text", height=180)

    elif input_type == "Voice (Audio Upload)":
        audio_file = st.file_uploader("Upload Audio (WAV / MP3)", type=["wav", "mp3"])
        if audio_file:
            input_text = audio_file_to_text(audio_file)
            st.text_area("Recognized Text", input_text, height=120)

    elif input_type == "Image":
        img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        if img_file:
            img = Image.open(img_file)
            st.image(img, use_column_width=True)
            input_text = ocr_image(img)
            st.text_area("Extracted Text", input_text, height=120)

    elif input_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf_file:
            input_text = ocr_pdf(pdf_file)
            st.text_area("Extracted Text", input_text, height=120)

    if st.button("🔄 Convert to Simple Tamil", type="primary"):
        if not input_text.strip():
            st.warning("Please provide input")
        else:
            detected = detect_language(input_text)
            tamil = translate_to_tamil(input_text)
            simple = simplify_tamil(tamil)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Original Text")
                st.markdown(f"**Detected Language:** `{detected}`")
                st.text_area("", input_text, height=200)

            with col2:
                st.markdown("### Simple Modern Tamil")
                st.text_area("", simple, height=200)

            st.download_button(
                "⬇️ Download Output",
                simple,
                file_name="simple_tamil.txt"
            )

# ================= PHASE 2 =================
with tab2:
    st.subheader("📖 Phase-2: Ancient / Old Tamil → Modern Tamil + Meaning")

    st.markdown(
        "Upload or paste **ancient Tamil poems / texts**. "
        "The system converts them into **modern Tamil with meanings** for students."
    )

    phase2_type = st.radio(
        "📥 Select Input Type",
        ["Text", "Image", "PDF", "Voice (Audio Upload)"],
        horizontal=True
    )

    ancient_text = ""

    if phase2_type == "Text":
        ancient_text = st.text_area(
            "Enter Ancient / Old Tamil Text",
            height=180,
            placeholder="யாதும் ஊரே யாவரும் கேளிர்"
        )

    elif phase2_type == "Image":
        img_file = st.file_uploader("Upload Ancient Tamil Image", type=["jpg", "png", "jpeg"])
        if img_file:
            img = Image.open(img_file)
            st.image(img, use_column_width=True)
            ancient_text = ocr_image(img)
            st.text_area("Extracted Text", ancient_text, height=120)

    elif phase2_type == "PDF":
        pdf_file = st.file_uploader("Upload Tamil PDF", type=["pdf"])
        if pdf_file:
            ancient_text = ocr_pdf(pdf_file)
            st.text_area("Extracted Text", ancient_text, height=120)

    elif phase2_type == "Voice (Audio Upload)":
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])
        if audio_file:
            ancient_text = audio_file_to_text(audio_file)
            st.text_area("Recognized Text", ancient_text, height=120)

    if st.button("📘 Convert to Modern Tamil & Explain", type="primary"):
        if not ancient_text.strip():
            st.warning("Please provide ancient Tamil input")
        else:
            modern = ancient_to_modern_tamil(ancient_text)
            meaning = generate_meaning(modern)

            st.markdown("### 🟤 Original Ancient Tamil")
            st.text_area("", ancient_text, height=120)

            st.markdown("### 🟢 Modern Simple Tamil")
            st.text_area("", modern, height=120)

            st.markdown("### 📘 Meaning / Explanation")
            st.text_area("", meaning, height=120)

            st.download_button(
                "⬇️ Download Explanation",
                meaning,
                file_name="ancient_tamil_explanation.txt"
            )

# ================= SIDEBAR =================
st.sidebar.title("ℹ️ Project Info")
st.sidebar.markdown(
    """
    **Dual-Phase Tamil Translation System**
    
    ✔ Simple Tamil for common people  
    ✔ Ancient Tamil learning for students  
    ✔ Text, Image, PDF, Audio support  
    ✔ Cloud-safe Streamlit app  
    """
)




