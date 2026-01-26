import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
from PIL import Image
import pytesseract
import tempfile
import av

st.set_page_config(page_title="Deep Tamil Translator", layout="wide")

# ---------------- AUDIO PROCESSOR ----------------
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = b""

    def recv(self, frame: av.AudioFrame):
        pcm = frame.to_ndarray()
        self.audio_data += pcm.tobytes()
        return frame

# ---------------- FUNCTIONS ----------------
def translate(text, target):
    translator = GoogleTranslator(source="auto", target=target)
    return translator.translate(text)

def improve_tamil(text):
    replacements = {
        "நான் இருக்கிறேன்": "நான் உள்ளேன்",
        "எனக்கு தெரியும்": "எனக்குத் தெரியும்",
        "நீங்கள் எப்படி இருக்கிறீர்கள்": "நீங்கள் எப்படி உள்ளீர்கள்"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def simple_english(text):
    return GoogleTranslator(source="auto", target="en").translate(text)

def text_to_voice(text, lang):
    tts = gTTS(text=text, lang=lang)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(file.name)
    return file.name

def create_pdf(inp, out):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, f"INPUT:\n{inp}\n\nOUTPUT:\n{out}")
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(file.name)
    return file.name

# ---------------- UI ----------------
st.title("🎙️ Any Language → Tamil / Simple English")

mode = st.radio("Input Mode", ["Text", "Mic", "Image"])

input_text = ""

# TEXT
if mode == "Text":
    input_text = st.text_area("Enter text", height=200)

# MIC
elif mode == "Mic":
    st.info("Click START and speak")
    ctx = webrtc_streamer(
        key="speech",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )
    if ctx.audio_processor:
        if st.button("Stop & Convert"):
            r = sr.Recognizer()
            audio = sr.AudioData(
                ctx.audio_processor.audio_data,
                sample_rate=44100,
                sample_width=2,
            )
            input_text = r.recognize_google(audio)
            st.success("Speech converted to text")
            st.write(input_text)

# IMAGE
elif mode == "Image":
    img_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if img_file:
        img = Image.open(img_file)
        input_text = pytesseract.image_to_string(img)
        st.success("Image converted to text")
        st.write(input_text)

# OUTPUT
if input_text:
    detected = detect(input_text)
    st.info(f"Detected Language: {detected}")

    out_lang = st.selectbox("Output Language", ["Tamil", "English"])

    if st.button("Translate"):
        if out_lang == "Tamil":
            output = improve_tamil(translate(input_text, "ta"))
            lang_code = "ta"
        else:
            output = simple_english(input_text)
            lang_code = "en"

        st.subheader("Output")
        st.success(output)

        if st.button("🔊 Voice Output"):
            audio = text_to_voice(output, lang_code)
            st.audio(audio)
            st.download_button("Download Voice", open(audio, "rb"), "output.mp3")

        if st.button("📄 Download PDF"):
            pdf = create_pdf(input_text, output)
            st.download_button("Download PDF", open(pdf, "rb"), "output.pdf")

        st.markdown("### Feedback")
        st.button("👍 Helpful")
        st.button("👎 Not Helpful")
