import streamlit as st
import numpy as np
import cv2
from PIL import Image
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ancient Tamil to Modern Tamil System",
    layout="wide"
)

st.title("🪔 Ancient Tamil → Modern Tamil Interpretation System")
st.caption("Dual Phase | User Translation + Archaeological Interpretation")

# ---------------- FUNCTIONS ----------------
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
    if len(text.strip()) == 0:
        return "FAILED"
    elif len(text) < 30:
        return "POOR"
    elif len(text) < 100:
        return "AVERAGE"
    else:
        return "GOOD"


def clean_ancient_text(text):
    words = text.split()
    return [w for w in words if len(w) > 2]


def ancient_to_modern(words):
    return " ".join(words)


def contextual_modern_tamil():
    return (
        "இந்த கல்வெட்டு கோவில், தானம் அல்லது அரசாணை தொடர்பான "
        "பழமையான தமிழ்ச் செய்தியை குறிக்கலாம். "
        "சில எழுத்துகள் அழிந்துள்ளதால், இது ஒரு "
        "பொதுவான நவீன தமிழ் விளக்கமாக வழங்கப்படுகிறது."
    )


def translate_to_tamil(text):
    try:
        return GoogleTranslator(source="auto", target="ta").translate(text)
    except:
        return text


def tamil_voice(text):
    tts = gTTS(text=text, lang="ta")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


# ---------------- MODE SELECTION ----------------
mode = st.radio(
    "Select Mode",
    ["🧑 Simple Tamil Translation",
     "🏺 Ancient Tamil → Modern Tamil"]
)

# ================= PHASE 1 =================
if mode == "🧑 Simple Tamil Translation":
    text = st.text_area("Enter any language text")

    if st.button("Convert to Simple Tamil"):
        if text.strip():
            out = translate_to_tamil(text)
            st.success("Modern Tamil Output")
            st.write(out)
            st.audio(tamil_voice(out))

# ================= PHASE 2 =================
if mode == "🏺 Ancient Tamil → Modern Tamil":

    uploaded = st.file_uploader(
        "Upload Ancient Tamil Image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded:
        img = Image.open(uploaded)
        img_np = np.array(img)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        processed = preprocess_image(img_np)
        ocr_text = safe_ocr(processed)
        quality = ocr_quality(ocr_text)

        st.subheader("🔍 OCR Analysis")
        st.write("OCR Quality:", quality)
        st.text_area("Raw OCR Output", ocr_text, height=120)

        # -------- OCR SUCCESS --------
        if quality in ["GOOD", "AVERAGE"]:
            cleaned = clean_ancient_text(ocr_text)
            modern = ancient_to_modern(cleaned)

            st.subheader("🟢 Modern Tamil (Interpreted)")
            st.write(modern)
            st.audio(tamil_voice(modern))

        # -------- OCR FAILED / POOR --------
        else:
            st.warning("OCR unreliable due to erosion or low image quality.")

            # OPTION A
            st.subheader("🅰️ Contextual Modern Tamil Interpretation")
            contextual = contextual_modern_tamil()
            st.write(contextual)
            st.audio(tamil_voice(contextual))

            # OPTION B
            st.subheader("🅱️ Expert-Assisted Conversion")
            manual = st.text_area(
                "Enter any visible ancient Tamil words"
            )

            if manual.strip():
                converted = translate_to_tamil(manual)
                st.success("Modern Tamil from Expert Input")
                st.write(converted)
                st.audio(tamil_voice(converted))

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Research Prototype | Ancient Tamil → Modern Tamil | OCR + Contextual AI"
)
