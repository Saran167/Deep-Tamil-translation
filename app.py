import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from gtts import gTTS
from fpdf import FPDF
import os
import uuid
import tempfile
import base64
from PIL import Image
import pytesseract
import time
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Universal Language Translator", 
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    
    .title-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-bottom: 30px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .input-box, .output-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #764ba2;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-box {
        background: rgba(40, 167, 69, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    
    .info-box {
        background: rgba(23, 162, 184, 0.1);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 10px 0;
    }
    
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
    }
    
    .step {
        text-align: center;
        padding: 15px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        flex: 1;
        margin: 0 10px;
    }
    
    .step-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }
    
    .highlight {
        background-color: #ffeb3b;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
    
    .language-badge {
        display: inline-block;
        padding: 5px 15px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
    }
    
    .feedback-btn {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px;
    }
    
    .feedback-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 65, 108, 0.4);
    }
    
    .download-btn {
        background: linear-gradient(45deg, #11998e, #38ef7d);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
    }
    
    .voice-btn {
        background: linear-gradient(45deg, #36D1DC, #5B86E5);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
    }
    
    .stProgress .st-bd {
        background-color: #764ba2;
    }
    
    .text-area-custom textarea {
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- INITIALIZATION --------------------
if 'translations' not in st.session_state:
    st.session_state.translations = []
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False

# -------------------- FUNCTIONS --------------------
def detect_language(text):
    """Detect the language of the input text"""
    try:
        lang_code = detect(text)
        # Map language codes to full names
        lang_map = {
            'ta': 'Tamil', 'en': 'English', 'hi': 'Hindi', 'ml': 'Malayalam',
            'te': 'Telugu', 'kn': 'Kannada', 'fr': 'French', 'es': 'Spanish',
            'de': 'German', 'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese',
            'ar': 'Arabic', 'ru': 'Russian'
        }
        return lang_map.get(lang_code, f"Unknown ({lang_code})")
    except LangDetectException:
        return "Unknown"

def simplify_english(text):
    """Simplify English text for better understanding"""
    # Simple word replacements for common complex words
    simplifications = {
        "utilize": "use", "facilitate": "help", "implement": "use",
        "endeavor": "try", "consequently": "so", "nevertheless": "but",
        "furthermore": "also", "consequently": "so", "subsequently": "later",
        "approximately": "about", "demonstrate": "show", "sufficient": "enough",
        "terminate": "end", "initiate": "start", "endeavour": "try",
        "ascertain": "find out", "elucidate": "explain", "procure": "get"
    }
    
    for complex_word, simple_word in simplifications.items():
        text = text.replace(f" {complex_word} ", f" {simple_word} ")
        text = text.replace(f" {complex_word.capitalize()} ", f" {simple_word.capitalize()} ")
    
    return text

def translate_to_tamil(text):
    """Translate text to Tamil using deep-translator"""
    try:
        translated = GoogleTranslator(source='auto', target='ta').translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def translate_to_english(text):
    """Translate text to English and simplify if needed"""
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        # Check if original was already English
        try:
            original_lang = detect(text)
            if original_lang == 'en':
                return simplify_english(translated)
        except:
            pass
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def improve_tamil_text(text):
    """Add highlights to improved Tamil words"""
    # This is a simplified version - in real scenario you'd have a dictionary
    # of improved translations
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

def chunk_text(text, max_length=500):
    """Split long text into chunks for better processing"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def tamil_voice_output(text, filename_prefix="tamil"):
    """Generate Tamil voice output"""
    try:
        chunks = chunk_text(text, max_length=100)  # Smaller chunks for TTS
        temp_files = []
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                tts = gTTS(text=chunk, lang='ta', slow=False)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{i}.mp3")
                tts.save(temp_file.name)
                temp_files.append(temp_file.name)
        
        # Combine audio files
        if temp_files:
            final_filename = f"{filename_prefix}_{uuid.uuid4().hex}.mp3"
            with open(final_filename, 'wb') as outfile:
                for temp_file in temp_files:
                    with open(temp_file, 'rb') as infile:
                        outfile.write(infile.read())
                    os.unlink(temp_file)
            return final_filename
    except Exception as e:
        st.error(f"Voice generation error: {str(e)}")
    return None

def english_voice_output(text, filename_prefix="english"):
    """Generate English voice output"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"{filename_prefix}_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Voice generation error: {str(e)}")
    return None

def create_styled_pdf(input_text, tamil_output, english_output, detected_lang):
    """Create a styled PDF with all information"""
    pdf = FPDF()
    pdf.add_page()
    
    # Add Unicode font
    try:
        pdf.add_font('Arial', '', 'arial.ttf', uni=True)
        pdf.set_font('Arial', '', 12)
    except:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
    
    # Header
    pdf.set_fill_color(102, 126, 234)  # Purple gradient color
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font_size(20)
    pdf.cell(0, 30, "Universal Language Translator", ln=True, align='C')
    
    # Reset color
    pdf.set_text_color(0, 0, 0)
    pdf.set_font_size(12)
    pdf.ln(20)
    
    # Metadata
    pdf.set_font_size(10)
    pdf.cell(0, 10, f"Translation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Detected Input Language: {detected_lang}", ln=True)
    pdf.ln(10)
    
    # Input Section
    pdf.set_font_size(14)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 10, "📝 Original Input Text:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font_size(11)
    pdf.multi_cell(0, 8, input_text)
    pdf.ln(10)
    
    # Tamil Output
    pdf.set_font_size(14)
    pdf.set_text_color(40, 167, 69)  # Green
    pdf.cell(0, 10, "🇮🇳 Tamil Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 8, tamil_output)
    pdf.ln(10)
    
    # English Output
    pdf.set_font_size(14)
    pdf.set_text_color(23, 162, 184)  # Blue
    pdf.cell(0, 10, "🇬🇧 English Translation:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 8, english_output)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font_size(10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, "Generated by Universal Language Translator", 0, 0, 'C')
    
    filename = f"translation_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(filename)
    return filename

def extract_text_from_image(image_file):
    """Extract text from uploaded image using OCR"""
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return None

def speech_to_text():
    """Convert speech to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now... Listening...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None

def record_feedback(rating, feedback_type):
    """Record user feedback"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_data = {
        'timestamp': timestamp,
        'rating': rating,
        'type': feedback_type,
        'input': st.session_state.get('last_input', ''),
        'tamil_output': st.session_state.get('last_tamil_output', ''),
        'english_output': st.session_state.get('last_english_output', '')
    }
    
    # In a real app, save to database
    st.session_state.feedback_given = True
    st.success(f"✅ Thank you for your {feedback_type} feedback!")
    
    # Save to local file (for demo)
    with open("feedback_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | Rating: {rating} | Type: {feedback_type}\n")
        f.write(f"Input: {feedback_data['input'][:100]}...\n")
        f.write("-" * 50 + "\n")

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px;'>
        <h1 style='color: white;'>🌐 Universal Translator</h1>
        <p style='color: rgba(255,255,255,0.9);'>Any Language → Tamil + English</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Features")
    features = """
    ✅ **Multi-Input Support:**
       - Text Input
       - Voice Input
       - Image Upload
    
    ✅ **Smart Output:**
       - Tamil Translation
       - Simple English
       - Language Detection
    
    ✅ **Enhanced Features:**
       - Text Highlighting
       - Voice Output
       - Styled PDF
       - Paragraph Support
    """
    st.markdown(features)
    
    st.markdown("---")
    
    st.markdown("### 📈 Statistics")
    if 'translation_count' not in st.session_state:
        st.session_state.translation_count = 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Translations", st.session_state.translation_count)
    with col2:
        st.metric("Feedback", len(st.session_state.translations))
    
    st.markdown("---")
    
    st.markdown("### ℹ️ How to Use")
    steps = """
    1. Choose input method
    2. Enter/speak/upload content
    3. View translations
    4. Listen/download results
    5. Provide feedback
    """
    st.markdown(steps)

# -------------------- MAIN INTERFACE --------------------
st.markdown("""
<div class='title-container'>
    <h1 style='color: white; text-align: center;'>🌐 Universal Language Translator</h1>
    <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 18px;'>
        Translate Any Language → Tamil & Simple English with Enhanced Features
    </p>
</div>
""", unsafe_allow_html=True)

# Steps visualization
st.markdown("""
<div class='step-container'>
    <div class='step'>
        <div class='step-icon'>📝</div>
        <h4>1. Input</h4>
        <p>Text, Voice or Image</p>
    </div>
    <div class='step'>
        <div class='step-icon'>🌐</div>
        <h4>2. Detect</h4>
        <p>Language Detection</p>
    </div>
    <div class='step'>
        <div class='step-icon'>🔄</div>
        <h4>3. Translate</h4>
        <p>Tamil + English</p>
    </div>
    <div class='step'>
        <div class='step-icon'>🎵</div>
        <h4>4. Output</h4>
        <p>Text + Voice + PDF</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Tabs
tab1, tab2, tab3 = st.tabs(["📝 Text Input", "🎤 Voice Input", "🖼️ Image Upload"])

input_text = ""
detected_language = ""

with tab1:
    st.markdown("### Enter Text in Any Language")
    input_text = st.text_area(
        "Type or paste your text here (paragraphs supported):",
        height=150,
        key="text_input_area",
        help="You can enter text in any language. Long paragraphs are supported."
    )
    
    if st.button("🔍 Detect & Translate", key="text_translate", use_container_width=True):
        if input_text:
            with st.spinner("Processing..."):
                # Detect language
                detected_language = detect_language(input_text)
                
                # Show detected language
                st.markdown(f"<div class='info-box'>🌍 Detected Language: <span class='language-badge'>{detected_language}</span></div>", unsafe_allow_html=True)
                
                # Store input
                st.session_state.last_input = input_text
                
                # Create output section
                st.markdown("<div class='output-box'>", unsafe_allow_html=True)
                st.markdown("### 📊 Translation Results")
                
                # Create columns for outputs
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🇮🇳 Tamil Translation")
                    tamil_translation = translate_to_tamil(input_text)
                    improved_tamil = improve_tamil_text(tamil_translation)
                    st.session_state.last_tamil_output = improved_tamil
                    
                    # Display with highlighting
                    st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(40, 167, 69, 0.05); border-radius: 10px;'>{improved_tamil}</div>", 
                              unsafe_allow_html=True)
                    
                    # Tamil Voice
                    if st.button("🔊 Tamil Voice", key="tamil_voice_text", use_container_width=True):
                        with st.spinner("Generating Tamil audio..."):
                            audio_file = tamil_voice_output(tamil_translation, "tamil_text")
                            if audio_file:
                                st.audio(audio_file, autoplay=True)
                                os.unlink(audio_file)
                
                with col2:
                    st.markdown("#### 🇬🇧 English Translation")
                    english_translation = translate_to_english(input_text)
                    st.session_state.last_english_output = english_translation
                    
                    st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(23, 162, 184, 0.05); border-radius: 10px;'>{english_translation}</div>", 
                              unsafe_allow_html=True)
                    
                    # English Voice
                    if st.button("🔊 English Voice", key="english_voice_text", use_container_width=True):
                        with st.spinner("Generating English audio..."):
                            audio_file = english_voice_output(english_translation, "english_text")
                            if audio_file:
                                st.audio(audio_file, autoplay=True)
                                os.unlink(audio_file)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download Section
                st.markdown("### 📥 Download Results")
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    if st.button("📄 Download PDF Report", use_container_width=True):
                        with st.spinner("Creating PDF..."):
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
                                    file_name=f"translation_{uuid.uuid4().hex[:8]}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            os.unlink(pdf_file)
                
                with col_d2:
                    if st.button("📝 Download Text Files", use_container_width=True):
                        # Create combined text file
                        text_content = f"""UNIVERSAL LANGUAGE TRANSLATOR
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
                
                # Increment counter
                st.session_state.translation_count += 1
        else:
            st.warning("⚠️ Please enter some text to translate.")

with tab2:
    st.markdown("### 🎤 Voice Input")
    st.markdown("Speak in any language, get Tamil and English translations")
    
    if st.button("🎤 Start Recording", key="voice_record", use_container_width=True):
        with st.spinner("Listening..."):
            voice_text = speech_to_text()
            
            if voice_text:
                input_text = voice_text
                st.markdown(f"<div class='success-box'>🎤 Recognized Speech: {voice_text}</div>", unsafe_allow_html=True)
                
                # Store input
                st.session_state.last_input = voice_text
                
                # Detect language
                detected_language = detect_language(voice_text)
                st.markdown(f"<div class='info-box'>🌍 Detected Language: <span class='language-badge'>{detected_language}</span></div>", unsafe_allow_html=True)
                
                # Show outputs (similar to text input)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🇮🇳 Tamil Translation")
                    tamil_translation = translate_to_tamil(voice_text)
                    improved_tamil = improve_tamil_text(tamil_translation)
                    st.session_state.last_tamil_output = improved_tamil
                    st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(40, 167, 69, 0.05); border-radius: 10px;'>{improved_tamil}</div>", 
                              unsafe_allow_html=True)
                    
                    if st.button("🔊 Tamil Voice", key="tamil_voice_speech", use_container_width=True):
                        audio_file = tamil_voice_output(tamil_translation, "tamil_voice")
                        if audio_file:
                            st.audio(audio_file, autoplay=True)
                            os.unlink(audio_file)
                
                with col2:
                    st.markdown("#### 🇬🇧 English Translation")
                    english_translation = translate_to_english(voice_text)
                    st.session_state.last_english_output = english_translation
                    st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(23, 162, 184, 0.05); border-radius: 10px;'>{english_translation}</div>", 
                              unsafe_allow_html=True)
                    
                    if st.button("🔊 English Voice", key="english_voice_speech", use_container_width=True):
                        audio_file = english_voice_output(english_translation, "english_voice")
                        if audio_file:
                            st.audio(audio_file, autoplay=True)
                            os.unlink(audio_file)
                
                # PDF Download
                if st.button("📄 Download PDF Report (Voice)", use_container_width=True):
                    pdf_file = create_styled_pdf(
                        voice_text, 
                        improved_tamil, 
                        english_translation, 
                        detected_language
                    )
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=f,
                            file_name="voice_translation.pdf",
                            mime="application/pdf"
                        )
                    os.unlink(pdf_file)
                
                st.session_state.translation_count += 1
            else:
                st.error("❌ Could not recognize speech. Please try again.")

with tab3:
    st.markdown("### 🖼️ Upload Image with Text")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("📖 Extract & Translate Text", key="image_translate", use_container_width=True):
            with st.spinner("Extracting text from image..."):
                extracted_text = extract_text_from_image(uploaded_file)
                
                if extracted_text and extracted_text.strip():
                    input_text = extracted_text
                    st.markdown(f"<div class='success-box'>📖 Extracted Text: {extracted_text[:200]}...</div>", unsafe_allow_html=True)
                    
                    # Store input
                    st.session_state.last_input = extracted_text
                    
                    # Detect language
                    detected_language = detect_language(extracted_text)
                    st.markdown(f"<div class='info-box'>🌍 Detected Language: <span class='language-badge'>{detected_language}</span></div>", unsafe_allow_html=True)
                    
                    # Show outputs
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🇮🇳 Tamil Translation")
                        tamil_translation = translate_to_tamil(extracted_text)
                        improved_tamil = improve_tamil_text(tamil_translation)
                        st.session_state.last_tamil_output = improved_tamil
                        st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(40, 167, 69, 0.05); border-radius: 10px;'>{improved_tamil}</div>", 
                                  unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("#### 🇬🇧 English Translation")
                        english_translation = translate_to_english(extracted_text)
                        st.session_state.last_english_output = english_translation
                        st.markdown(f"<div style='font-size: 16px; line-height: 1.8; padding: 15px; background: rgba(23, 162, 184, 0.05); border-radius: 10px;'>{english_translation}</div>", 
                                  unsafe_allow_html=True)
                    
                    st.session_state.translation_count += 1
                else:
                    st.error("❌ Could not extract text from image. Please ensure the image contains clear text.")

# -------------------- FEEDBACK SECTION --------------------
st.markdown("---")
st.markdown("### 💬 Feedback & Rating")

if st.session_state.get('last_input'):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        if st.button("👍 Good Translation", use_container_width=True):
            record_feedback(5, "Good")
    
    with col_f2:
        if st.button("👎 Needs Improvement", use_container_width=True):
            record_feedback(2, "Needs Improvement")
    
    with col_f3:
        if st.button("⭐ Excellent!", use_container_width=True):
            record_feedback(5, "Excellent")
    
    # Detailed feedback
    with st.expander("Provide Detailed Feedback"):
        detailed_feedback = st.text_area("Your detailed feedback:", height=100)
        if st.button("Submit Detailed Feedback"):
            if detailed_feedback:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("detailed_feedback.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{timestamp}\n")
                    f.write(f"Feedback: {detailed_feedback}\n")
                    f.write(f"Input: {st.session_state.last_input[:100]}...\n")
                    f.write("-" * 50 + "\n")
                st.success("✅ Thank you for your detailed feedback!")
else:
    st.info("Make a translation first to provide feedback!")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(0,0,0,0.05); border-radius: 10px;'>
    <p style='color: #666;'>
        🌐 <strong>Universal Language Translator</strong> | 
        Any Language → Tamil + Simple English |
        With Voice & Document Support
    </p>
    <p style='color: #999; font-size: 14px;'>
        Supports long paragraphs • Language detection • Enhanced Tamil output • Simple English • Multiple output formats
    </p>
</div>
""", unsafe_allow_html=True)
