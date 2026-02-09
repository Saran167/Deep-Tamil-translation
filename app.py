import streamlit as st
from PIL import Image
import pdfplumber
import easyocr
from deep_translator import GoogleTranslator

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Ancient Tamil → Simple Modern Tamil")
st.caption("For TNPSC • Tamil Poems • Old Tamil Learning")

# ---------------- OCR INITIALIZATION ----------------
@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(
        ['ta', 'en'],
        gpu=False,
        verbose=False
    )

try:
    reader = load_ocr_reader()
except Exception:
    st.error("❌ OCR engine failed to load. Please reboot the app once.")
    st.stop()

# ---------------- OCR FUNCTIONS ----------------
def ocr_from_image(image):
    results = reader.readtext(image)
    text_lines = [res[1] for res in results]
    return "\n".join(text_lines)

def ocr_from_pdf(pdf_file):
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
    return extracted_text.strip()

# ---------------- TEXT PROCESSING ----------------
def split_poem_lines(text):
    return [line.strip() for line in text.split("\n") if len(line.strip()) > 3]

def simple_tamil(line):
    # placeholder for future custom simplification logic
    return line

def meaning_in_simple_english(line):
    try:
        return GoogleTranslator(source="ta", target="en").translate(line)
    except:
        return "Meaning not available"

# ---------------- UI INPUT ----------------
st.subheader("📥 Upload / Enter Ancient Tamil")

input_mode = st.radio(
    "Choose Input Type",
    ["Image", "PDF", "Text"],
    horizontal=True
)

raw_text = ""

if input_mode == "Image":
    img_file = st.file_uploader(
        "Upload Tamil Poem Image",
        type=["png", "jpg", "jpeg"]
    )
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        with st.spinner("🔍 Reading Tamil text from image..."):
            raw_text = ocr_from_image(image)

elif input_mode == "PDF":
    pdf_file = st.file_uploader(
        "Upload Tamil PDF",
        type=["pdf"]
    )
    if pdf_file:
        with st.spinner("📄 Reading text from PDF..."):
            raw_text = ocr_from_pdf(pdf_file)

else:
    raw_text = st.text_area(
        "Paste Ancient Tamil Text",
        height=250,
        placeholder="தமிழ் செய்யுள் / பழைய உரை இங்கே ஒட்டவும்..."
    )

# ---------------- OUTPUT ----------------
if raw_text:
    st.subheader("📜 Extracted Tamil Text")
    st.text_area("", raw_text, height=180)

    st.subheader("🧠 Line-by-Line Explanation (TNPSC Friendly)")

    lines = split_poem_lines(raw_text)

    for idx, line in enumerate(lines, start=1):
        with st.expander(f"📖 Line {idx}"):
            st.markdown(f"**🕰️ Ancient Tamil:**  \n{line}")
            st.markdown(f"**✅ Simple Tamil:**  \n{simple_tamil(line)}")
            st.markdown(f"**📘 Meaning (Easy English):**  \n{meaning_in_simple_english(line)}")

else:
    st.info("👆 Upload an image / PDF or paste text to begin.")






