import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
from fpdf import FPDF
import os
import uuid
from PIL import Image
import pytesseract
import datetime
import tempfile
import io

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
    
    /* Info boxes */
    .info-box {
        background: rgba(23, 162, 184, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 15px 0;
    }
    
    .success-box {
        background: rgba(40, 167, 69, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
    
    .warning-box {
        background: rgba(255, 193, 7, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 15px 0;
    }
    
    /* Audio upload box */
    .audio-upload-box {
        background: rgba(54, 209, 220, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #36D1DC;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'translations' not in st.session_state:
    st.session_state.translations = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

# -------------------- FUNCTIONS --------------------
def detect_language(text):
    """Detect input language"""
    try:
        lang_code = detect(text)
        lang_map = {
            'ta': 'Tamil', 'en': 'English', 'hi': 'Hindi', 'ml': 'Malayalam',
            'te': 'Telugu', 'kn': 'Kannada', 'fr': 'French', 'es': 'Spanish',
            'de': 'German', 'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese',
            'ru': 'Russian', 'ar': 'Arabic', 'it': 'Italian', 'pt': 'Portuguese'
        }
        return lang_map.get(lang_code, f"Language ({lang_code})")
    except Exception as e:
        return "Unknown"

def translate_to_tamil(text):
    """Translate text to Tamil"""
    try:
        translated = GoogleTranslator(source='auto', target='ta').translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def translate_to_english(text):
    """Translate text to English"""
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def simplify_english(text):
    """Simplify English text for better understanding"""
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
        "initiate": "start",
        "ascertain": "find out",
        "elucidate": "explain",
        "procure": "get"
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
        "புரிந்து": "💡புரிந்து💡",
        "கிடைக்கும்": "✅கிடைக்கும்✅",
        "உதவும்": "🤝உதவும்🤝",
        "சிறந்த": "🏆சிறந்த🏆",
        "வேகமாக": "⚡வேகமாக⚡"
    }
    
    for phrase, improved in improved_phrases.items():
        text = text.replace(phrase, improved)
    
    return text

def tamil_voice_output(text):
    """Generate Tamil voice output"""
    try:
        tts = gTTS(text=text, lang='ta', slow=False)
        filename = f"tamil_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Voice generation error: {str(e)}")
    return None

def english_voice_output(text):
    """Generate English voice output"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"english_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Voice generation error: {str(e)}")
    return None

def create_styled_pdf(input_text, tamil_output, english_output, detected_lang):
    """Create a styled PDF with all information"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(102, 126, 234)  # Purple color
    pdf.cell(0, 15, "Universal Language Translator", ln=True, align='C')
    
    # Date and info
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 8, f"Detected Language: {detected_lang}", ln=True)
    pdf.ln(10)
    
    # Original text
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "📝 Original Text:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, input_text)
    pdf.ln(10)
    
    # Tamil translation
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(255, 0, 0)  # Red for Tamil
    pdf.cell(0, 10, "🇮🇳 Tamil Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, tamil_output)
    pdf.ln(10)
    
    # English translation
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 255)  # Blue for English
    pdf.cell(0, 10, "🇬🇧 English Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, english_output)
    
    filename = f"translation_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(filename)
    return filename

def extract_text_from_image(image_file):
    """Extract text from uploaded image"""
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None

def process_audio_file(audio_file):
    """Process uploaded audio file for speech recognition"""
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name
        
        # Use speech recognition on the audio file
        r = sr.Recognizer()
        with sr.AudioFile(tmp_file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        return text
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
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
        <div class="step-icon">📝🎤🖼️</div>
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
        help="You can enter text in any language - long paragraphs are supported",
        key="text_input_main"
    )
    
    if st.button("Translate Text", key="text_translate", use_container_width=True):
        if input_text.strip():
            detected_language = detect_language(input_text)
            st.session_state.input_text = input_text
            st.session_state.detected_language = detected_language
            st.session_state.translation_ready = True
        else:
            st.warning("Please enter some text to translate")

with tab2:
    st.markdown("### 🎤 Voice Input Options")
    
    # Option 1: Audio file upload
    st.markdown('<div class="audio-upload-box">', unsafe_allow_html=True)
    st.markdown("#### Option 1: Upload Audio File")
    st.markdown("Record your voice using any app (like Voice Recorder) and upload it")
    
    uploaded_audio = st.file_uploader(
        "Choose audio file (WAV, MP3, M4A)",
        type=['wav', 'mp3', 'm4a', 'ogg'],
        key="audio_upload"
    )
    
    if uploaded_audio is not None:
        # Show audio player
        st.audio(uploaded_audio)
        
        if st.button("🎵 Transcribe Audio File", key="transcribe_audio", use_container_width=True):
            with st.spinner("Converting audio to text..."):
                transcribed_text = process_audio_file(uploaded_audio)
                if transcribed_text:
                    st.session_state.voice_text = transcribed_text
                    st.session_state.input_text = transcribed_text
                    st.session_state.detected_language = detect_language(transcribed_text)
                    st.session_state.translation_ready = True
                    st.success(f"✅ Transcribed: {transcribed_text[:200]}...")
                else:
                    st.error("Could not transcribe audio. Please try a clearer recording.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Option 2: Text simulation
    st.markdown("#### Option 2: Type Your Speech")
    st.markdown("Type what you would say into the microphone")
    
    simulated_voice = st.text_area(
        "Enter your speech text here:",
        height=100,
        key="simulated_voice",
        placeholder="Type what you want to translate..."
    )
    
    if st.button("🎤 Use as Voice Input", key="use_simulated", use_container_width=True):
        if simulated_voice.strip():
            st.session_state.input_text = simulated_voice
            st.session_state.detected_language = detect_language(simulated_voice)
            st.session_state.translation_ready = True
            st.success("✅ Voice input simulated successfully!")
        else:
            st.warning("Please enter some text")
    
    # Option 3: Sample phrases
    st.markdown("#### Option 3: Try Sample Phrases")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        if st.button("Hello, how are you?", key="sample1", use_container_width=True):
            st.session_state.input_text = "Hello, how are you today?"
            st.session_state.detected_language = "English"
            st.session_state.translation_ready = True
            st.rerun()
    
    with col_s2:
        if st.button("I want to learn Tamil", key="sample2", use_container_width=True):
            st.session_state.input_text = "I want to learn Tamil language"
            st.session_state.detected_language = "English"
            st.session_state.translation_ready = True
            st.rerun()
    
    with col_s3:
        if st.button("Translate this please", key="sample3", use_container_width=True):
            st.session_state.input_text = "Please translate this sentence to Tamil"
            st.session_state.detected_language = "English"
            st.session_state.translation_ready = True
            st.rerun()

with tab3:
    st.markdown("### 🖼️ Upload Image with Text")
    uploaded_file = st.file_uploader("Choose an image file (PNG, JPG, JPEG)", type=['png', 'jpg', 'jpeg'], key="image_uploader")
    
    if uploaded_file is not None:
        col_img, col_info = st.columns([2, 1])
        with col_img:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col_info:
            if st.button("Extract & Translate Text", key="image_extract", use_container_width=True):
                with st.spinner("Extracting text from image..."):
                    extracted_text = extract_text_from_image(uploaded_file)
                    if extracted_text and extracted_text.strip():
                        input_text = extracted_text
                        detected_language = detect_language(extracted_text)
                        st.session_state.input_text = input_text
                        st.session_state.detected_language = detected_language
                        st.session_state.translation_ready = True
                        st.success(f"✅ Text extracted successfully!")
                    else:
                        st.error("Could not extract text from image. Please ensure the image contains clear text.")

st.markdown('</div>', unsafe_allow_html=True)

# Check if we have input text for translation
if 'translation_ready' in st.session_state and st.session_state.translation_ready:
    input_text = st.session_state.input_text
    detected_language = st.session_state.detected_language
    
    # Translation Results
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Translation Results</div>', unsafe_allow_html=True)
    
    # Show detected language
    st.markdown(f'<div class="info-box">'
                f'🌍 <b>Detected Language:</b> <span class="language-badge">{detected_language}</span></div>', 
                unsafe_allow_html=True)
    
    # Process translations
    with st.spinner("Translating..."):
        # Translate to Tamil
        tamil_translation = translate_to_tamil(input_text)
        improved_tamil = improve_tamil_text(tamil_translation)
        
        # Translate to English
        english_translation = translate_to_english(input_text)
        if detected_language == "English":
            english_translation = simplify_english(input_text)
    
    col_tamil, col_english = st.columns(2)
    
    with col_tamil:
        st.markdown('<div class="tamil-output">', unsafe_allow_html=True)
        st.markdown("#### 🇮🇳 Tamil Translation")
        
        # Display Tamil text
        st.markdown(f'<div style="font-size: 18px; line-height: 1.8; padding: 15px; background: rgba(255,107,107,0.05); border-radius: 10px;">'
                   f'{improved_tamil}</div>', unsafe_allow_html=True)
        
        # Tamil voice button
        col_voice1, col_dl1 = st.columns(2)
        with col_voice1:
            if st.button("🔊 Listen Tamil", key="tamil_voice", use_container_width=True):
                with st.spinner("Generating Tamil audio..."):
                    audio_file = tamil_voice_output(tamil_translation)
                    if audio_file:
                        st.audio(audio_file, autoplay=False)
                        try:
                            os.unlink(audio_file)
                        except:
                            pass
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_english:
        st.markdown('<div class="english-output">', unsafe_allow_html=True)
        st.markdown("#### 🇬🇧 English Translation")
        
        # Display English text
        st.markdown(f'<div style="font-size: 18px; line-height: 1.8; padding: 15px; background: rgba(54, 209, 220, 0.05); border-radius: 10px;">'
                   f'{english_translation}</div>', unsafe_allow_html=True)
        
        # English voice button
        col_voice2, col_dl2 = st.columns(2)
        with col_voice2:
            if st.button("🔊 Listen English", key="english_voice", use_container_width=True):
                with st.spinner("Generating English audio..."):
                    audio_file = english_voice_output(english_translation)
                    if audio_file:
                        st.audio(audio_file, autoplay=False)
                        try:
                            os.unlink(audio_file)
                        except:
                            pass
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📥 Download Results</div>', unsafe_allow_html=True)
    
    col_pdf, col_txt = st.columns(2)
    
    with col_pdf:
        if st.button("📄 Download PDF Report", key="pdf_download", use_container_width=True):
            with st.spinner("Creating PDF document..."):
                pdf_file = create_styled_pdf(
                    input_text, 
                    improved_tamil, 
                    english_translation, 
                    detected_language
                )
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=f"translation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        key="pdf_dl_btn",
                        use_container_width=True
                    )
                try:
                    os.unlink(pdf_file)
                except:
                    pass
    
    with col_txt:
        if st.button("📝 Download Text File", key="txt_download", use_container_width=True):
            # Create text content
            text_content = f"""UNIVERSAL LANGUAGE TRANSLATOR
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Original Text ({detected_language}):
{'-'*50}
{input_text}

Tamil Translation (with improvements):
{'-'*50}
{improved_tamil}

English Translation:
{'-'*50}
{english_translation}

Note: ✨⭐🎯 symbols highlight improved Tamil translations
"""
            st.download_button(
                label="⬇️ Download Text",
                data=text_content,
                file_name=f"translation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="txt_dl_btn",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feedback Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 Feedback & Rating</div>', unsafe_allow_html=True)
    
    st.markdown("How was your translation experience?")
    
    col_good, col_avg, col_poor = st.columns(3)
    
    with col_good:
        if st.button("👍 Good", key="fb_good", use_container_width=True):
            st.session_state.feedback.append({
                "rating": "good", 
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "input": input_text[:100]
            })
            st.success("Thank you for your feedback! 👍")
            st.balloons()
    
    with col_avg:
        if st.button("👌 Average", key="fb_avg", use_container_width=True):
            st.session_state.feedback.append({
                "rating": "average",
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "input": input_text[:100]
            })
            st.success("Thank you for your feedback! 👌")
    
    with col_poor:
        if st.button("👎 Needs Improvement", key="fb_poor", use_container_width=True):
            st.session_state.feedback.append({
                "rating": "poor",
                "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "input": input_text[:100]
            })
            st.success("Thank you for your feedback! We'll improve. 👎")
    
    # Show feedback stats
    if st.session_state.feedback:
        st.markdown("---")
        good_count = len([f for f in st.session_state.feedback if f['rating'] == 'good'])
        avg_count = len([f for f in st.session_state.feedback if f['rating'] == 'average'])
        poor_count = len([f for f in st.session_state.feedback if f['rating'] == 'poor'])
        
        st.markdown(f"**Feedback Statistics:** 👍 {good_count} | 👌 {avg_count} | 👎 {poor_count}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Store in history
    st.session_state.translations.append({
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "input": input_text[:200],
        "tamil": improved_tamil[:200],
        "english": english_translation[:200],
        "language": detected_language
    })

# Translation History (Collapsible)
with st.expander("📚 View Translation History"):
    if st.session_state.translations:
        for i, trans in enumerate(reversed(st.session_state.translations[-5:]), 1):
            st.markdown(f"""
            **Translation {i}** ({trans['timestamp']})
            - **Language:** {trans['language']}
            - **Input:** {trans['input']}...
            - **Tamil:** {trans['tamil']}...
            - **English:** {trans['english']}...
            ---
            """)
    else:
        st.info("No translation history yet.")

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.8); margin-top: 50px;">
    <hr style="border-color: rgba(255,255,255,0.2);">
    <h3 style="color: white;">🌐 Universal Language Translator</h3>
    <p><b>Any Language → Tamil + Simple English</b></p>
    <div style="display: flex; justify-content: center; gap: 20px; margin: 15px 0; flex-wrap: wrap;">
        <span>✅ Multi-input Support</span>
        <span>✅ Language Detection</span>
        <span>✅ Enhanced Tamil</span>
        <span>✅ Simple English</span>
        <span>✅ Voice Output</span>
        <span>✅ PDF Export</span>
        <span>✅ Image OCR</span>
        <span>✅ Feedback System</span>
    </div>
    <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-top: 20px;">
        Supports long paragraphs • Highlighted improvements • All languages supported • Perfect for academic projects
    </p>
</div>
""", unsafe_allow_html=True)
