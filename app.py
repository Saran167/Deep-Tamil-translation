import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from PIL import Image
import tempfile, os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Talk2Tamil",
    page_icon="🗣️",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style="text-align:center;">🗣️ Talk2Tamil – Human Friendly Translator</h1>
<p style="text-align:center;">
📝 Text | 🎤 Voice | 🖼️ Image → 🇮🇳 Tamil / 🇬🇧 Simple English
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def simplify_english(text):
    replacements = {
        "utilize": "use",
        "approximately": "about",
        "commence": "start",
        "terminate": "end",
        "assistance": "help",
        "individuals": "people",
        "numerous": "many",
        "purchase": "buy",
        "demonstrate": "show"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def better_tamil(text):
    replacements = {
        "பயன்படுத்து": "உபயோகி",
        "தொடங்குக": "ஆரம்பி",
        "நிறைவேற்ற": "முடி",
        "பரிசீலனை": "ஆலோசனை",
        "அடையாளம் காண": "கண்டுபிடி",
        "முன்னெச்சரிக்கை": "ஜாக்கிரதை",
        "செயல்படுத்த": "செய்"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def translate(text, output_lang):
    if output_lang == "🇮🇳 Tamil":
        ta = GoogleTranslator(source="auto", target="ta").translate(text)
        return better_tamil(ta)
    else:
        if text.isascii():
            return simplify_english(text)
        else:
            en = GoogleTranslator(source="auto", target="en").translate(text)
            return simplify_english(en)

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang="ta" if lang=="🇮🇳 Tamil" else "en")
    filename = "output.mp3"
    tts.save(filename)
    return filename

def create_doc(original, translated):
    return f"""
Talk2Tamil – Translation Output
Generated: {datetime.now()}

---------------------------
INPUT:
{original}

---------------------------
OUTPUT:
{translated}
"""

# ---------------- INPUT TABS ----------------
tab1, tab2, tab3 = st.tabs(["📝 Text", "🎤 Voice", "🖼️ Image"])

# TEXT INPUT
with tab1:
    text_input = st.text_area("📝 Enter text (any language)", height=180)
    if text_input:
        st.session_state.input_text = text_input

# VOICE INPUT
with tab2:
    audio = st.audio_input("🎤 Speak now")
    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio.getbuffer())
            path = f.name
        r = sr.Recognizer()
        try:
            with sr.AudioFile(path) as source:
                data = r.record(source)
                voice_text = r.recognize_google(data)
            st.success("Voice recognized")
            st.text_area("Detected text", voice_text)
            st.session_state.input_text = voice_text
        except:
            st.error("Could not recognize voice")
        os.remove(path)

# IMAGE INPUT
with tab3:
    img = st.file_uploader("🖼️ Upload image", type=["png","jpg","jpeg"])
    if img:
        st.image(Image.open(img), width=250)
        img_text = st.text_area("✍️ Type text from image")
        if img_text:
            st.session_state.input_text = img_text

# ---------------- OUTPUT SETTINGS ----------------
st.markdown("---")
output_lang = st.radio(
    "🎯 Choose output language",
    ["🇮🇳 Tamil", "🇬🇧 Simple English"],
    horizontal=True
)

voice_out = st.checkbox("🔊 Voice output", value=True)
doc_out = st.checkbox("📄 Download document", value=True)

# ---------------- TRANSLATE ----------------
if st.button("✨ TRANSLATE", use_container_width=True):
    if "input_text" not in st.session_state:
        st.warning("Please give input")
    else:
        with st.spinner("Processing..."):
            result = translate(st.session_state.input_text, output_lang)

        st.subheader("✅ Output")
        st.success(result)

        if voice_out:
            audio = text_to_speech(result, output_lang)
            st.audio(audio)

        if doc_out:
            doc = create_doc(st.session_state.input_text, result)
            st.download_button(
                "📄 Download",
                doc,
                file_name="Talk2Tamil_Output.txt"
            )

st.markdown("<hr><center>Final Year Project – Phase 2</center>", unsafe_allow_html=True)
