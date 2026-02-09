import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Tamil Learning Assistant",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Tamil Learning Assistant")
st.write(
    "Convert **Tamil poems, lessons, or chapters** into "
    "**simple, student-friendly modern Tamil**."
)

# ------------------ FUNCTIONS ------------------
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def simplify_tamil_text(text):
    prompt = f"""
    கீழே உள்ள தமிழ் பாடல் அல்லது பாட உரையை
    மாணவர்கள் எளிதாக புரிந்துகொள்ளும்
    நவீன எளிய தமிழ் மொழியாக மாற்றி விளக்கவும்.

    உரை:
    {text}
    """
    return GoogleTranslator(source="auto", target="ta").translate(prompt)

# ------------------ UI ------------------
uploaded_file = st.file_uploader(
    "📤 Upload Tamil PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    extracted_text = ""

    if uploaded_file.type == "application/pdf":
        st.subheader("📄 Extracted Text (PDF)")
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Original Tamil Text", extracted_text, height=200)

    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.info(
            "✍️ OCR for Tamil images is assisted.\n"
            "Please paste or correct the extracted Tamil text below."
        )

        extracted_text = st.text_area(
            "Paste / Correct Tamil Text from Image",
            height=200
        )

    if extracted_text.strip():
        st.subheader("📘 Simple Modern Tamil Explanation")
        simplified = simplify_tamil_text(extracted_text)
        st.text_area(
            "Student-Friendly Tamil",
            simplified,
            height=250
        )

st.markdown("---")
st.caption("🎓 Designed for Tamil learners & education-focused interpretation")




