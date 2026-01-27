import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from fpdf import FPDF
import os
import uuid
from PIL import Image
import pytesseract
import tempfile

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Universal Language Translator", 
    page_icon="🌐",
    layout="wide"
)

# Custom CSS for colorful UI
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 30px;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 25px;
        border-left: 6px solid #764ba2;
    }
    
    /* Section headers */
    .section-header {
        color: #764ba2;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Step labels */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
    }
    
    .step {
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        flex: 1;
        margin: 0 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .step:hover {
        transform: translateY(-5px);
    }
    
    .step-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
        color: #764ba2;
    }
    
    .step-number {
        background: #764ba2;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        font-weight: bold;
    }
    
    /* Language badges */
    .language-badge {
        display: inline-block;
        padding: 6px 15px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 5px;
    }
    
    /* Output boxes */
    .output-box {
        background: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #28a745;
    }
    
    .tamil-output {
        border-left: 5px solid #ff6b6b;
    }
    
    .english-output {
        border-left: 5px solid #36D1DC;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .voice-btn {
        background: linear-gradient(45deg, #36D1DC, #5B86E5) !important;
    }
    
    .image-btn {
        background: linear-gradient(45deg, #11998e, #38ef7d) !important;
    }
    
    .download-btn {
        background: linear-gradient(45deg, #FF416C, #FF4B2B) !important;
    }
    
    /* Highlight text */
    .highlight {
        background-color: #ffeb3b;
        padding: 2px 5px;
        border-radius: 3px;
        font-weight: bold;
    }
    
    /* Feedback buttons */
    .feedback-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }
    
    .feedback-btn {
        padding: 10px 25px;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .feedback-good {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
    }
    
    .feedback-average {
        background: linear-gradient(45deg, #ff9966, #ff5e62);
        color: white;
    }
    
    .feedback-poor {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
    }
    
    /* Text areas */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 16px;
        padding: 15px;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'translations' not in st.session_state:
    st.session_state.translations = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# -------------------- FUNCTIONS --------------------
def speech_to_text():
    """Your original speech recognition function - NOT CHANGED"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now... Listening...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None

def detect_language(text):
    """Simple language detection"""
    try:
        from langdetect import detect
        lang_code = detect(text)
        lang_map = {
            'ta': 'Tamil', 'en': 'English', 'hi': 'Hindi', 'ml': 'Malayalam',
            'te': 'Telugu', 'kn': 'Kannada', 'fr': 'French', 'es': 'Spanish',
            'de': 'German', 'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese'
        }
        return lang_map.get(lang_code, f"Unknown ({lang_code})")
    except:
        return "Unknown"

def translate_to_tamil(text):
    translator = Translator()
    translated = translator.translate(text, dest='ta')
    return translated.text

def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    return translated.text

def simplify_english(text):
    """Simplify English text"""
    simplifications = {
        "utilize": "use",
        "facilitate": "help", 
        "implement": "use",
        "endeavor": "try",
        "consequently": "so",
        "nevertheless": "but",
        "approximately": "about",
        "demonstrate": "show",
        "sufficient": "enough",
        "terminate": "end",
        "initiate": "start"
    }
    
    for complex_word, simple_word in simplifications.items():
        text = text.replace(f" {complex_word} ", f" {simple_word} ")
        text = text.replace(f" {complex_word.capitalize()} ", f" {simple_word.capitalize()} ")
    
    return text

def improve_tamil_text(text):
    """Add highlights to improved Tamil words"""
    improved_phrases = {
        "முடியும்": "✨முடியும்✨",
        "செய்ய": "⭐செய்ய⭐", 
        "பெற": "🎯பெற🎯",
        "அறிய": "🔍அறிய🔍",
        "புரிந்து": "💡புரிந்து💡"
    }
    
    for phrase, improved in improved_phrases.items():
        text = text.replace(phrase, improved)
    
    return text

def tamil_voice_output(text):
    filename = f"tamil_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='ta')
    tts.save(filename)
    return filename

def english_voice_output(text):
    filename = f"english_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def create_pdf(input_text, tamil_text, english_text, detected_lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Universal Language Translator", ln=True, align='C')
    pdf.ln(10)
    
    # Input section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Original Text ({detected_lang}):", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, input_text)
    pdf.ln(10)
    
    # Tamil output
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 0, 0)  # Red for Tamil
    pdf.cell(0, 10, "Tamil Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, tamil_text)
    pdf.ln(10)
    
    # English output
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 255)  # Blue for English
    pdf.cell(0, 10, "English Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, english_text)
    
    filename = f"translation_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(filename)
    return filename

def extract_text_from_image(image_file):
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None

# -------------------- MAIN INTERFACE --------------------
st.markdown('<div class="main-title">🌐 Universal Language Translator</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.9); font-size: 1.2rem;">Any Language → Tamil & Simple English with Enhanced Features</p>', unsafe_allow_html=True)

# Steps visualization
st.markdown('<div class="step-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('''
    <div class="step">
        <div class="step-number">1</div>
        <div class="step-icon">📝</div>
        <h4>Input Method</h4>
        <p>Text, Voice or Image</p>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div class="step">
        <div class="step-number">2</div>
        <div class="step-icon">🌐</div>
        <h4>Language Detection</h4>
        <p>Auto-detect input language</p>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown('''
    <div class="step">
        <div class="step-number">3</div>
        <div class="step-icon">🔄</div>
        <h4>Smart Translation</h4>
        <p>Tamil + Simple English</p>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown('''
    <div class="step">
        <div class="step-number">4</div>
        <div class="step-icon">🎵📄</div>
        <h4>Output Options</h4>
        <p>Voice + Text + PDF</p>
    </div>
    ''', unsafe_allow_html=True)
    
st.markdown('</div>', unsafe_allow_html=True)

# Input Methods
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📥 Choose Input Method</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Text Input", "🎤 Voice Input", "🖼️ Image Upload"])

input_text = ""
detected_language = "Unknown"

with tab1:
    st.markdown("### Enter Text in Any Language")
    input_text = st.text_area(
        "Type or paste your text (paragraphs supported):",
        height=150,
        help="You can enter text in any language"
    )
    
    if st.button("Translate Text", key="text_translate", use_container_width=True):
        if input_text:
            detected_language = detect_language(input_text)

with tab2:
    st.markdown("### 🎤 Voice Input")
    st.markdown("Click below to start recording")
    
    if st.button("Start Recording", key="voice_record", use_container_width=True):
        with st.spinner("Listening... Please speak now..."):
            voice_text = speech_to_text()
            if voice_text:
                input_text = voice_text
                st.success(f"✅ Recognized: {voice_text}")
                detected_language = detect_language(voice_text)
            else:
                st.error("Could not recognize speech. Please try again.")

with tab3:
    st.markdown("### 🖼️ Upload Image with Text")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Extract Text from Image", key="image_extract", use_container_width=True):
            with st.spinner("Extracting text..."):
                extracted_text = extract_text_from_image(uploaded_file)
                if extracted_text:
                    input_text = extracted_text
                    st.success(f"✅ Text extracted: {extracted_text[:200]}...")
                    detected_language = detect_language(extracted_text)
                else:
                    st.error("Could not extract text from image")

st.markdown('</div>', unsafe_allow_html=True)

# Translation Results
if input_text:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Translation Results</div>', unsafe_allow_html=True)
    
    # Show detected language
    st.markdown(f'<div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">'
                f'🌍 <b>Detected Language:</b> <span class="language-badge">{detected_language}</span></div>', 
                unsafe_allow_html=True)
    
    col_tamil, col_english = st.columns(2)
    
    with col_tamil:
        st.markdown('<div class="tamil-output">', unsafe_allow_html=True)
        st.markdown("#### 🇮🇳 Tamil Translation")
        
        # Translate to Tamil
        tamil_translation = translate_to_tamil(input_text)
        improved_tamil = improve_tamil_text(tamil_translation)
        
        # Display with highlights
        st.markdown(f'<div style="font-size: 18px; line-height: 1.8; padding: 15px; background: rgba(255,107,107,0.05); border-radius: 10px;">'
                   f'{improved_tamil}</div>', unsafe_allow_html=True)
        
        # Tamil voice
        if st.button("🔊 Tamil Voice", key="tamil_voice", use_container_width=True):
            with st.spinner("Generating Tamil audio..."):
                audio_file = tamil_voice_output(tamil_translation)
                if audio_file:
                    st.audio(audio_file, autoplay=True)
                    os.unlink(audio_file)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_english:
        st.markdown('<div class="english-output">', unsafe_allow_html=True)
        st.markdown("#### 🇬🇧 English Translation")
        
        # Translate to English
        english_translation = translate_to_english(input_text)
        
        # If original was English, simplify it
        if detected_language == "English":
            english_translation = simplify_english(input_text)
        
        st.markdown(f'<div style="font-size: 18px; line-height: 1.8; padding: 15px; background: rgba(54, 209, 220, 0.05); border-radius: 10px;">'
                   f'{english_translation}</div>', unsafe_allow_html=True)
        
        # English voice
        if st.button("🔊 English Voice", key="english_voice", use_container_width=True):
            with st.spinner("Generating English audio..."):
                audio_file = english_voice_output(english_translation)
                if audio_file:
                    st.audio(audio_file, autoplay=True)
                    os.unlink(audio_file)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📥 Download Results</div>', unsafe_allow_html=True)
    
    col_pdf, col_txt = st.columns(2)
    
    with col_pdf:
        if st.button("📄 Download PDF Report", use_container_width=True):
            with st.spinner("Creating PDF..."):
                pdf_file = create_pdf(input_text, improved_tamil, english_translation, detected_language)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=f"translation_{uuid.uuid4().hex[:8]}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                os.unlink(pdf_file)
    
    with col_txt:
        if st.button("📝 Download Text Files", use_container_width=True):
            # Create text content
            text_content = f"""UNIVERSAL LANGUAGE TRANSLATOR
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Original Text ({detected_language}):
{'-'*50}
{input_text}

Tamil Translation:
{'-'*50}
{improved_tamil}

English Translation:
{'-'*50}
{english_translation}
"""
            st.download_button(
                label="⬇️ Download Text",
                data=text_content,
                file_name="translations.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feedback Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 Feedback</div>', unsafe_allow_html=True)
    
    st.markdown("How was your translation experience?")
    
    col_good, col_avg, col_poor = st.columns(3)
    
    with col_good:
        if st.button("👍 Good", use_container_width=True, key="fb_good"):
            st.session_state.feedback.append({"rating": "good", "text": input_text[:100]})
            st.success("Thank you for your feedback! 👍")
    
    with col_avg:
        if st.button("👌 Average", use_container_width=True, key="fb_avg"):
            st.session_state.feedback.append({"rating": "average", "text": input_text[:100]})
            st.success("Thank you for your feedback! 👌")
    
    with col_poor:
        if st.button("👎 Needs Improvement", use_container_width=True, key="fb_poor"):
            st.session_state.feedback.append({"rating": "poor", "text": input_text[:100]})
            st.success("Thank you for your feedback! 👎")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.8); margin-top: 50px;">
    <hr style="border-color: rgba(255,255,255,0.2);">
    <p>🌐 <b>Universal Language Translator</b> | Any Language → Tamil + Simple English | With Voice & Document Support</p>
    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">
        Features: Multi-input support • Language detection • Enhanced Tamil output • Simple English • Voice output • PDF download
    </p>
</div>
""", unsafe_allow_html=True)
