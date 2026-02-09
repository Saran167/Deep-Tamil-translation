import streamlit as st
from PIL import Image
import pdfplumber
from deep_translator import GoogleTranslator
import easyocr

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Ancient Tamil → Modern Tamil + Meaning")
st.caption("TNPSC • Poems • Old Tamil Learning")

# ---------------- OCR (SAFE INITIALIZATION) ----------------
@st.experimental_singleton
def init_ocr():
    return easyocr.Reader(
        ['ta', 'en'],
        gpu=False,
        verbose=False
    )

try:
    reader = init_ocr()
except Exception as e:
    st.error("OCR Engine failed to load. Please refresh once.")
    st.stop()

# ---------------- OCR FUNCTIONS ----------------
def ocr_image(image):
    results = reader.readtext(image)
    return "\n".join([r[1] for r in results])

def ocr_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# ---------------- TEXT LOGIC ----------------
def split_lines(text):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 3]
    return lines

def simplify_tamil(line):
    try:
        return GoogleTranslator(source="ta", target="ta").translate(line)
    except:
        return line

def explain_meaning(line):
    try:
        return GoogleTranslator(source="ta", target="en").translate(line)
    except:
        return "Meaning unavailable"

# ---------------- UI ----------------
st.subheader("📥 Input Ancient Tamil")

mode = st.radio("Input Type", ["Image", "PDF", "Text"], horizontal=True)

raw_text = ""

if mode == "Image":
    img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if img:
        image = Image.open(img)
        st.image(image, use_column_width=True)
        with st.spinner("Reading Tamil text..."):
            raw_text = ocr_image(image)

elif mode == "PDF":
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if pdf:
        with st.spinner("Reading PDF..."):
            raw_text = ocr_pdf(pdf)

else:
    raw_text = st.text_area("Paste Ancient Tamil Text", height=250)

# ---------------- OUTPUT ----------------
if raw_text:
    st.subheader("📜 Extracted Text")
    st.text_area("", raw_text, height=180)

    st.subheader("🧠 Line-by-Line Explanation")

    for i, line in enumerate(split_lines(raw_text), 1):
        with st.expander(f"📖 Line {i}"):
            st.markdown(f"**Ancient Tamil:** {line}")
            st.markdown(f"**Simple Tamil:** {simplify_tamil(line)}")
            st.markdown(f"**Meaning:** {explain_meaning(line)}")
else:
    st.info("Upload or paste text to start.")





