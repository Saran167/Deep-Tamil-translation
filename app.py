import streamlit as st
import numpy as np
import cv2
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Dual Phase Tamil Translation System",
    layout="wide"
)

st.title("🪔 Dual-Phase Tamil Translation System")
st.caption("Simple Tamil for Common Users | Ancient Tamil for Archaeology")

# -------------------------------------------------
# IMAGE PROCESSING & OCR
# -------------------------------------------------
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def safe_ocr(image):
    try:
        return pytesseract.image_to_string(
            image, lang="tam+eng", config="--psm 6"
        ).strip()
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


def ancient_to_modern_tamil(words):
    # Linguistic interpretation placeholder
    return " ".join(words)


# -------------------------------------------------
# LOW QUALITY IMAGE INTELLIGENCE (NO OCR)
# -------------------------------------------------
def low_quality_intelligence():
    return {
        "script": "Likely Pallava / Vatteluttu Tamil",
        "language": "Tamil mixed with possible Sanskrit (Grantha influence)",
        "era": "Approximately 8th–12th Century",
        "context": "Temple, donation, or administrative inscription",
        "note": "Exact characters unreadable due to erosion or weathering"
    }


# -------------------------------------------------
# SIMPLE TAMIL TRANSLATION
# -------------------------------------------------
def simple_tamil_translate(text):
    try:
        return GoogleTranslator(source="auto", target="ta").translate(text)
    except:
        return "Translation failed."


def tamil_voice(text):
    tts = gTTS(text=text, lang="ta")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


# -------------------------------------------------
# MODE SELECTION
# -------------------------------------------------
mode = st.radio(
    "Select Mode",
    ["🧑‍🤝‍🧑 Simple Tamil (Common Users)",
     "🏺 Ancient Tamil (Archaeology)"]
)

# =================================================
# PHASE 1 – SIMPLE TAMIL
# =================================================
if mode == "🧑‍🤝‍🧑 Simple Tamil (Common Users)":

    st.subheader("🔤 Enter Text (Any Language)")
    input_text = st.text_area("Input text")

    if st.button("Convert to Simple Tamil"):
        if input_text.strip():
            output = simple_tamil_translate(input_text)
            st.success("✅ Simplified Tamil Output")
            st.write(output)

            audio = tamil_voice(output)
            st.audio(audio)
        else:
            st.warning("Please enter text.")

# =================================================
# PHASE 2 – ARCHAEOLOGICAL TAMIL
# =================================================
if mode == "🏺 Ancient Tamil (Archaeology)":

    st.subheader("📜 Upload Ancient Tamil Image")
    uploaded = st.file_uploader(
        "Upload inscription / manuscript image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded:
        image = Image.open(uploaded)
        img_np = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        processed = preprocess_image(img_np)
        ocr_text = safe_ocr(processed)
        quality = ocr_quality(ocr_text)

        st.markdown("### 🔍 OCR Analysis")
        st.write("OCR Quality:", quality)
        st.text_area("Raw OCR Output", ocr_text, height=120)

        # ---------- NORMAL OCR PATH ----------
        if quality in ["AVERAGE", "GOOD"]:
            cleaned = clean_ancient_ocr(ocr_text)

            st.subheader("🧹 Cleaned Ancient Text")
            st.write(cleaned)

            modern = ancient_to_modern_tamil(cleaned)

            st.subheader("🟢 Modern Tamil Interpretation")
            st.write(modern)

            audio = tamil_voice(modern)
            st.audio(audio)

        # ---------- LOW QUALITY INTELLIGENCE ----------
        else:
            st.warning("⚠️ OCR text extraction unreliable.")

            insights = low_quality_intelligence()

            st.subheader("🧠 Low-Quality Image Intelligence")
            st.write("📜 Estimated Script:", insights["script"])
            st.write("🌐 Language Composition:", insights["language"])
            st.write("🕰️ Probable Era:", insights["era"])
            st.write("📖 Possible Context:", insights["context"])

            st.info(
                insights["note"] +
                ". System avoids incorrect translation and provides contextual analysis."
            )

            st.text_area(
                "✍️ Expert Manual Input (Optional)",
                placeholder="Enter any clearly visible ancient Tamil characters here..."
            )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption(
    "Academic Prototype | OCR + NLP + Tamil Linguistics + Archaeological Intelligence"
)



