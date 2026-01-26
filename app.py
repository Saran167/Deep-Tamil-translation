import streamlit as st
from langdetect import detect
from transformers import pipeline
from gtts import gTTS
from fpdf import FPDF
import tempfile
import datetime
import re

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Tamil–English Translator",
    page_icon="🌈",
    layout="wide"
)

# --------------------------------------------------
# UI STYLING
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #fbc2eb, #a6c1ee);
}
.block {
    background: white;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}
.highlight {
    color: #2e7d32;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE + STEPS
# --------------------------------------------------
st.title("🌈 Smart Spoken Tamil & Simple English Translator")

st.markdown("""
📥 **Input** → 🔁 **Process** → 📤 **Output** → 📄 **Download**
""")

# --------------------------------------------------
# LOAD TRANSLATOR (SAFE)
# --------------------------------------------------
@st.cache_resource
def load_translator():
    return pipeline("translation", model="facebook/m2m100_418M")

translator = load_translator()

# --------------------------------------------------
# SPOKEN TAMIL RULES
# --------------------------------------------------
spoken_tamil_map = {
    "நான்": "நா",
    "உங்களை": "உங்க",
    "உங்களுக்கு": "உங்க",
    "அழைப்பேன்": "கால் பண்ணுறேன்",
    "அனுப்புவேன்": "அனுப்பிடுறேன்",
    "தகவல்": "விஷயம்",
    "உடனடியாக": "உடனே",
    "இருக்கிறது": "இருக்கு",
    "நாளை": "நாளைக்கு"
}

# --------------------------------------------------
# SIMPLE ENGLISH RULES
# --------------------------------------------------
simple_english_map = {
    "kindly": "please",
    "ensure": "make sure",
    "prior to": "before",
    "assist": "help",
    "purchase": "buy",
    "utilize": "use",
    "commence": "start",
    "terminate": "end"
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def highlight_changes(original, modified, replacements):
    result = modified
    for k, v in replacements.items():
        if v in result:
            result = result.replace(v, f"<span class='highlight'>{v}</span>")
    return result

def chunk_text(text, size=300):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) <= size:
            current += " " + s
        else:
            chunks.append(current)
            current = s
    chunks.append(current)
    return chunks

def translate_chunks(text, target):
    chunks = chunk_text(text)
    outputs = []
    for c in chunks:
        out = translator(c, src_lang="auto", tgt_lang=target)[0]["translation_text"]
        outputs.append(out)
    return " ".join(outputs)

# --------------------------------------------------
# PDF GENERATION
# --------------------------------------------------
def create_pdf(input_text, output_text, in_lang, out_lang):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Smart Tamil–English Translator", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now()}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 10, f"{in_lang} → {out_lang}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 8, "INPUT:\n" + input_text)
    pdf.ln(4)
    pdf.multi_cell(0, 8, "OUTPUT:\n" + output_text)

    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)
    return file.name

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
st.markdown("<div class='block'>", unsafe_allow_html=True)
input_text = st.text_area("📝 Enter text in ANY language")
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# OUTPUT LANGUAGE
# --------------------------------------------------
output_lang = st.radio("🌐 Select Output Language", ["Tamil", "English"], horizontal=True)

# --------------------------------------------------
# PROCESS
# --------------------------------------------------
if st.button("✨ Convert"):
    if input_text.strip() == "":
        st.warning("Please enter text")
    else:
        detected_lang = detect(input_text)
        st.info(f"🌐 Detected Input Language: {detected_lang}")

        # TRANSLATION
        if output_lang == "Tamil":
            translated = translate_chunks(input_text, "ta")
            final_output = translated
            for k, v in spoken_tamil_map.items():
                final_output = final_output.replace(k, v)
            highlighted = highlight_changes(translated, final_output, spoken_tamil_map)

        else:
            translated = translate_chunks(input_text, "en")
            final_output = translated
            for k, v in simple_english_map.items():
                final_output = final_output.replace(k, v)
            highlighted = highlight_changes(translated, final_output, simple_english_map)

        # OUTPUT DISPLAY
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("📤 Output")
        st.markdown(highlighted, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # AUDIO OUTPUT
        tts = gTTS(final_output, lang="ta" if output_lang == "Tamil" else "en")
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio_file.name)
        st.audio(audio_file.name)

        # PDF DOWNLOAD
        pdf_path = create_pdf(input_text, final_output, detected_lang, output_lang)
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF", f, file_name="output.pdf")

        # FEEDBACK
        st.markdown("### 🗳️ Feedback")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Easy to understand"):
                st.success("Thank you for your feedback!")
        with col2:
            if st.button("👎 Needs improvement"):
                st.success("Thank you! We’ll improve it.")
