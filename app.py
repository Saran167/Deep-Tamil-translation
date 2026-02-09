import streamlit as st
import easyocr
from PIL import Image
import pdfplumber
from deep_translator import GoogleTranslator
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil + Meaning",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Ancient Tamil → Modern Tamil Learning Assistant")
st.caption("TNPSC • Poems • Old Literature • Student Friendly")

# ---------------- OCR SETUP ----------------
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['ta', 'en'], gpu=False)

ocr_reader = load_ocr()

# ---------------- OCR FUNCTIONS ----------------
def ocr_image(img):
    results = ocr_reader.readtext(img)
    text = "\n".join([res[1] for res in results])
    return text.strip()

def ocr_pdf(pdf_file):
    full_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text.strip()

# ---------------- LINE SPLIT LOGIC ----------------
def split_poem_lines(text):
    lines = text.split("\n")
    clean_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 3:
            clean_lines.append(line)
    return clean_lines

# ---------------- TRANSLATION LOGIC ----------------
def ancient_to_simple_tamil(line):
    try:
        simple = GoogleTranslator(source="ta", target="ta").translate(line)
    except:
        simple = line
    return simple

def tamil_meaning(line):
    try:
        meaning = GoogleTranslator(source="ta", target="en").translate(line)
    except:
        meaning = "Meaning unavailable"
    return meaning

# ---------------- UI INPUT ----------------
st.subheader("📥 Upload Ancient Tamil Content")

input_mode = st.radio(
    "Choose Input Type",
    ["Image", "PDF", "Text"],
    horizontal=True
)

raw_text = ""

if input_mode == "Image":
    img_file = st.file_uploader("Upload Tamil Image", type=["png", "jpg", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        with st.spinner("Reading ancient Tamil text..."):
            raw_text = ocr_image(image)

elif input_mode == "PDF":
    pdf_file = st.file_uploader("Upload Tamil PDF", type=["pdf"])
    if pdf_file:
        with st.spinner("Extracting text from PDF..."):
            raw_text = ocr_pdf(pdf_file)

elif input_mode == "Text":
    raw_text = st.text_area("Paste Ancient Tamil Text Here", height=250)

# ---------------- PROCESSING ----------------
if raw_text:
    st.subheader("📜 Extracted Ancient Tamil")
    st.text_area("", raw_text, height=200)

    poem_lines = split_poem_lines(raw_text)

    st.subheader("🧠 Line-by-Line Modern Tamil Explanation")

    for idx, line in enumerate(poem_lines, start=1):
        simple = ancient_to_simple_tamil(line)
        meaning = tamil_meaning(line)

        with st.expander(f"📖 Line {idx}"):
            st.markdown(f"**Ancient Tamil:** {line}")
            st.markdown(f"**Simple Modern Tamil:** {simple}")
            st.markdown(f"**Meaning (for students):** {meaning}")

else:
    st.info("Upload or paste Ancient Tamil content to begin.")




