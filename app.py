import streamlit as st
import easyocr
from PIL import Image
import numpy as np
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Tamil Learning Assistant",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Tamil Learning Assistant")
st.write(
    "Upload **Tamil poem / lesson image or PDF** and get "
    "**simple, modern Tamil explanation for students**."
)

# ------------------ OCR SETUP ------------------
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ta', 'en'], gpu=False)

reader = load_reader()

# ------------------ FUNCTIONS ------------------
def extract_text_from_image(image):
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0, paragraph=True)
    return "\n".join(results)

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def simplify_tamil_text(text):
    """
    Converts classical / poetic / complex Tamil
    into simple modern Tamil for students
    """
    try:
        prompt = f"""
        கீழே உள்ள தமிழ் உரையை
        மாணவர்கள் எளிதாக புரிந்துகொள்ளும்
        நவீன எளிய தமிழ் உரையாக மாற்றி விளக்கவும்.

        உரை:
        {text}
        """
        simplified = GoogleTranslator(
            source="auto",
            target="ta"
        ).translate(prompt)
        return simplified
    except:
        return text

# ------------------ UI ------------------
uploaded_file = st.file_uploader(
    "📤 Upload Tamil Image or PDF",
    type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        st.subheader("📄 Extracted Text (PDF)")
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Original Tamil Text", extracted_text, height=200)
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)
        st.subheader("📝 Extracted Tamil Text")
        st.text_area("Original Tamil Text", extracted_text, height=200)

    if extracted_text.strip():
        st.subheader("📘 Simple Modern Tamil Explanation")
        simplified_text = simplify_tamil_text(extracted_text)
        st.text_area(
            "Student-Friendly Tamil",
            simplified_text,
            height=250
        )
    else:
        st.warning("No readable Tamil text found.")

st.markdown("---")
st.caption("🎓 Designed for Tamil learners & students")



