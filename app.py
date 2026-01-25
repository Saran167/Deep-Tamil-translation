import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Talk2Tamil – Voice Translator",
    page_icon="🎤",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;'>🗣️ Talk2Tamil – Smart Voice Translator</h1>
<p style='text-align:center;'>
Any Language ➜ <b>Perfect Tamil</b> | Voice + Text | Download
</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def translate_to_tamil(text):
    return GoogleTranslator(source="auto", target="ta").translate(text)

def text_to_speech(text, lang="ta"):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "output.mp3"
    tts.save(filename)
    return filename

def create_document(original, tamil):
    content = f"""
Talk2Tamil – Translation Result
Generated on: {datetime.now()}

----------------------------------
ORIGINAL TEXT:
{original}

----------------------------------
TAMIL TRANSLATION:
{tamil}

----------------------------------
"""
    return content

# ---------------- INPUT TABS ----------------
tab1, tab2 = st.tabs(["🎤 Voice Input", "📝 Text Input"])

# ---------------- VOICE INPUT ----------------
with tab1:
    st.subheader("🎤 Record Your Voice (Browser Mic)")

    audio = st.audio_input("Click and speak clearly")

    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio.getbuffer())
            audio_path = f.name

        r = sr.Recognizer()
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = r.record(source)
                voice_text = r.recognize_google(audio_data, language="en-IN")

            st.success("✅ Voice recorded successfully")
            st.text_area("Recognized Text", voice_text, height=120)

            st.session_state["input_text"] = voice_text

        except:
            st.error("❌ Could not recognize voice. Try again.")

        os.remove(audio_path)

# ---------------- TEXT INPUT ----------------
with tab2:
    st.subheader("📝 Type or Paste Text")

    text_input = st.text_area(
        "Enter text in any language",
        height=180,
        placeholder="Example: Agriculture improves farmers income..."
    )

    if text_input:
        st.session_state["input_text"] = text_input

# ---------------- TRANSLATION ----------------
st.markdown("---")
if st.button("✨ TRANSLATE TO TAMIL", use_container_width=True):
    if "input_text" not in st.session_state or not st.session_state["input_text"].strip():
        st.warning("⚠️ Please provide input text or voice")
    else:
        with st.spinner("Translating..."):
            original_text = st.session_state["input_text"]
            tamil_text = translate_to_tamil(original_text)

        st.subheader("🇮🇳 Tamil Translation")
        st.success(tamil_text)

        # Voice output
        audio_file = text_to_speech(tamil_text)
        st.audio(audio_file)

        # Document download
        doc_content = create_document(original_text, tamil_text)
        st.download_button(
            "📄 Download as Text File",
            doc_content,
            file_name="Talk2Tamil_Output.txt"
        )

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<p style='text-align:center; font-size:14px;'>
Built using Streamlit | Voice + Tamil NLP Project
</p>
""", unsafe_allow_html=True)
