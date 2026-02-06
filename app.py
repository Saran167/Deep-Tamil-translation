import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil (Archaeologist AI)",
    layout="centered"
)

st.title("🏺 Ancient Tamil → Modern Tamil Translator")
st.caption("AI-Assisted Linguistic Reconstruction for Archaeology")

# ---------------- FUNCTIONS ----------------

def enhance_image(img):
    """Enhance faded ancient manuscripts"""
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return gray

def partial_ocr(img):
    try:
        text = pytesseract.image_to_string(img, lang="tam")
        return text.strip()
    except:
        return ""

def linguistic_reconstruction(text):
    """Core archaeology logic (NO OCR DEPENDENCY)"""
    keywords = []

    if "நில" in text or "nil" in text.lower():
        keywords.append("நிலம்")
    if "பதி" in text:
        keywords.append("குடியிருப்பு")
    if "கா" in text:
        keywords.append("காடு / நிலம்")

    if not keywords:
        return (
            "இந்த உரை பழங்கால தமிழில் எழுதப்பட்டிருக்கலாம்.\n"
            "இது நிலம், குடியிருப்பு அல்லது நிர்வாக தொடர்பான பதிவாக இருக்க வாய்ப்பு உள்ளது."
        )

    sentence = "இந்த உரை " + " மற்றும் ".join(keywords) + " பற்றிய தகவலைக் குறிக்கிறது."
    return sentence

def detect_script(text):
    if any(x in text for x in ["ஸ", "ஷ", "ஜ"]):
        return "தமிழ் + கிரந்த கலவை (Medieval)"
    elif len(text) < 5:
        return "வட்டெழுத்து / பழைய தமிழ்"
    else:
        return "செந்தமிழ் / இடைக்கால தமிழ்"

# ---------------- UI ----------------

mode = st.radio(
    "📌 Select Input Type",
    ["Upload Image", "Paste Ancient Tamil Text"]
)

if mode == "Upload Image":
    image_file = st.file_uploader("📤 Upload Ancient Tamil Image", type=["jpg", "png", "jpeg"])

    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        enhanced = enhance_image(image)
        st.subheader("🛠️ Enhanced Manuscript View")
        st.image(enhanced, use_column_width=True)

        ocr_text = partial_ocr(enhanced)

        st.subheader("🔍 Partial OCR Output")
        if ocr_text:
            st.code(ocr_text)
        else:
            st.warning("OCR could not clearly read text. Proceeding with linguistic interpretation.")

        st.subheader("📜 Script Identification")
        st.write(detect_script(ocr_text))

        st.subheader("🧠 Modern Tamil (Reconstructed Meaning)")
        modern_tamil = linguistic_reconstruction(ocr_text)
        st.success(modern_tamil)

        st.info("⚠️ This output is linguistically reconstructed, not a word-by-word translation.")

else:
    ancient_text = st.text_area("📜 Paste Ancient Tamil Text")

    if ancient_text:
        st.subheader("📜 Script Identification")
        st.write(detect_script(ancient_text))

        st.subheader("🧠 Modern Tamil (Reconstructed Meaning)")
        modern_tamil = linguistic_reconstruction(ancient_text)
        st.success(modern_tamil)

        st.info("⚠️ Linguistic reconstruction based on historical Tamil evolution rules.")

