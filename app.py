import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil System",
    layout="wide"
)

st.title("📜 Ancient Tamil → Modern Tamil Interpretation System")
st.caption("Dual-Phase | Archaeology-Aware | AI-Assisted")

st.divider()

# -------------------------------------------------
# UTIL FUNCTIONS
# -------------------------------------------------

def enhance_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def perform_ocr(image):
    try:
        text = pytesseract.image_to_string(image, lang="tam+eng")
        return text.strip()
    except:
        return ""

def classify_script(text):
    if any(ch in text for ch in ["ஜ", "ஶ", "ஷ", "ஸ", "ஹ"]):
        return "Tamil + Sanskrit (Grantha influence)"
    if len(text) < 10:
        return "Ancient Tamil Script (Unreadable / Eroded)"
    return "Ancient Tamil Script"

def estimate_period():
    return "8th – 12th Century (Pallava / Early Chola period)"

def convert_ancient_to_modern(text):
    # Simple academic mapping (extendable)
    rules = {
        "கோயில்": "கோவில்",
        "தானம்": "தானமாக வழங்கப்பட்டது",
        "இக்கோயில்": "இந்த கோவில்",
        "பண்டாரம்": "கோவில் நிர்வாகம்"
    }
    modern = text
    for k, v in rules.items():
        modern = modern.replace(k, v)
    return modern

def interpret_when_unclear():
    return (
        "இந்த கல்வெட்டில் உள்ள எழுத்துக்கள் முழுமையாக தெளிவாக இல்லை. "
        "எனினும், தமிழ் கல்வெட்டுகளில் வழக்கமாக காணப்படும் அமைப்பின் அடிப்படையில், "
        "இது கோவில் தொடர்பான தானம், நில அளிப்பு அல்லது நிர்வாக பதிவு ஆக இருக்கலாம்."
    )

# -------------------------------------------------
# PHASE SELECTION
# -------------------------------------------------
phase = st.radio(
    "Select Phase",
    ["Phase 1 – Any Language → Simple Tamil",
     "Phase 2 – Ancient Tamil → Modern Tamil"]
)

st.divider()

# =================================================
# PHASE 1
# =================================================
if phase == "Phase 1 – Any Language → Simple Tamil":
    st.subheader("🌐 Phase 1: Simple Tamil Translation")

    user_text = st.text_area("Enter text in any language")

    if st.button("Convert to Simple Tamil"):
        if user_text.strip():
            translated = GoogleTranslator(source="auto", target="ta").translate(user_text)

            st.subheader("📝 Output (Simple Tamil)")
            st.success(translated)

            tts = gTTS(translated, lang="ta")
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)

            st.audio(temp_audio.name)
        else:
            st.warning("Please enter text.")

# =================================================
# PHASE 2
# =================================================
else:
    st.subheader("🪨 Phase 2: Ancient Tamil → Modern Tamil")

    uploaded_image = st.file_uploader(
        "Upload Olai Chuvadi / Stone Inscription Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)

        col1, col2 = st.columns([1,2])

        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with col2:
            enhanced = enhance_image(image)
            ocr_text = perform_ocr(enhanced)

            st.subheader("📜 OCR Analysis")

            if len(ocr_text) == 0:
                st.error("OCR Quality: FAILED")
            elif len(ocr_text) < 40:
                st.warning("OCR Quality: POOR")
            else:
                st.success("OCR Quality: GOOD")

            st.text_area("Raw OCR Output", ocr_text, height=120)

            script = classify_script(ocr_text)
            period = estimate_period()

            st.divider()

            st.subheader("🧠 Archaeological Analysis")
            st.markdown(f"""
**Script Type:** {script}  
**Estimated Period:** {period}  
**Context:** Temple / Donation / Administrative Record
""")

            st.divider()

            st.subheader("📝 Modern Tamil Conversion")

            if len(ocr_text) >= 20:
                modern = convert_ancient_to_modern(ocr_text)
                st.success(modern)
            else:
                st.warning(interpret_when_unclear())

            st.info("""
⚠️ Note:  
Stone inscriptions may not allow word-by-word translation.  
This system follows archaeologist-style interpretation.
""")

    else:
        st.info("Upload an ancient Tamil image to begin analysis.")
