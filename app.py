import streamlit as st
from PIL import Image
import pytesseract
import json
import numpy as np

# ----------------------------
# Load ancient-modern mapping
# ----------------------------
with open("ancient_modern_map.json", "r", encoding="utf-8") as f:
    WORD_MAP = json.load(f)

# ----------------------------
# Helper Functions
# ----------------------------
def extract_text_from_image(image):
    try:
        return pytesseract.image_to_string(image, lang="tam")
    except:
        return ""

def convert_ancient_to_modern(text):
    modern_lines = []
    words = text.split()

    for w in words:
        clean = w.strip(".,;:!?()[]{}")
        modern = WORD_MAP.get(clean, clean)
        modern_lines.append(modern)

    return " ".join(modern_lines)

def archaeological_inference():
    return (
        "இந்த உரை பழைய தமிழில் எழுதப்பட்டுள்ளது. "
        "சில பகுதிகள் தெளிவாக இல்லாவிட்டாலும், "
        "இது சமூக அல்லது கோவில் தொடர்பான பதிவாக இருக்க வாய்ப்பு உள்ளது."
    )

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Ancient Tamil → Modern Tamil", layout="centered")
st.title("🏺 Ancient Tamil → Simple Modern Tamil Converter")

st.markdown("இந்த செயலி பழைய தமிழ் உரைகளை எளிய இன்றைய தமிழாக மாற்றுகிறது.")

input_type = st.radio("உள்ளீடு வகை தேர்வு செய்யவும்", ["Text", "Image"])

ancient_text = ""

if input_type == "Text":
    ancient_text = st.text_area("பழைய தமிழ் உரை இங்கே உள்ளிடவும்")

else:
    img_file = st.file_uploader("பழைய தமிழ் படம் பதிவேற்றவும்", type=["jpg", "png", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        ancient_text = extract_text_from_image(image)

# ----------------------------
# Processing
# ----------------------------
if st.button("மாற்று (Convert)"):
    if ancient_text.strip() == "":
        st.warning("உரை தெளிவாக இல்லை. ஆனால் விளக்கமாக மாற்ற முயற்சிக்கப்படுகிறது.")

        st.subheader("🧠 விளக்கமான பொருள் (Inference)")
        st.write(archaeological_inference())

    else:
        st.subheader("📜 கண்டறியப்பட்ட பழைய தமிழ்")
        st.write(ancient_text)

        modern = convert_ancient_to_modern(ancient_text)

        st.subheader("✅ எளிய இன்றைய தமிழ்")
        st.success(modern)

        st.caption("⚠️ இது சொல்-சொல்லாக மொழிபெயர்ப்பு அல்ல. மொழியியல் மறுஉருவாக்கம்.")

