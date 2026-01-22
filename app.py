import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import io
import base64
from datetime import datetime
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Visual Translator",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLES ====================
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 1rem;
    }
    
    /* Header styles */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid;
    }
    
    .feature-tamil {
        border-left-color: #FF6B6B;
    }
    
    .feature-english {
        border-left-color: #4ECDC4;
    }
    
    .feature-voice {
        border-left-color: #FFD166;
    }
    
    .feature-doc {
        border-left-color: #06D6A0;
    }
    
    /* Language output boxes */
    .lang-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .tamil-box {
        background: linear-gradient(135deg, #FFEAA7 0%, #FFD166 100%);
        border: 2px solid #FFB142;
    }
    
    .english-box {
        background: linear-gradient(135deg, #A8E6CF 0%, #4ECDC4 100%);
        border: 2px solid #06D6A0;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* Custom radio buttons */
    div[data-baseweb="radio"] div {
        background-color: #F8F9FA;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== APP HEADER ====================
st.markdown("""
<div class="app-header">
    <h1 style="font-size: 2.5rem; margin: 0;">🗣️ Talk2Tamil</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Visual Translation Assistant for Everyone</p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
        <span>🌍 Any Language →</span>
        <span>🇮🇳 Tamil</span>
        <span>🇬🇧 Simple English</span>
        <span>🔊 Voice</span>
        <span>📄 Documents</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FEATURE CARDS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card feature-tamil">
        <h3>🇮🇳 Tamil Translation</h3>
        <p>Accurate Tamil translations for any text</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card feature-english">
        <h3>🇬🇧 Simple English</h3>
        <p>Easy-to-understand English for learners</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card feature-voice">
        <h3>🔊 Voice Output</h3>
        <p>Listen to translations in clear voice</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card feature-doc">
        <h3>📄 Document Ready</h3>
        <p>Download as PDF or text files</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
st.markdown("---")
st.markdown("## 🚀 Let's Get Started")

# Initialize session state
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_output' not in st.session_state:
    st.session_state.current_output = None

# Functions (same as before - keep your existing functions)
def translate_to_tamil(text):
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        return translator.translate(text)
    except:
        return text

def simplify_english(text):
    # Your existing simplification dictionary
    simplification_dict = {
        'approximately': 'about',
        'utilize': 'use',
        'terminate': 'end',
        'commence': 'start',
        'purchase': 'buy',
        'acquire': 'get',
        # Add more as needed
    }
    simplified = text
    for complex_word, simple_word in simplification_dict.items():
        simplified = simplified.replace(complex_word, simple_word)
    return simplified

def generate_tamil_audio(text, filename="tamil_audio.mp3"):
    try:
        tts = gTTS(text=text, lang='ta', slow=False)
        tts.save(filename)
        return filename
    except:
        return None

def generate_english_audio(text, filename="english_audio.mp3"):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except:
        return None

# ==================== INPUT SECTION ====================
col_input, col_settings = st.columns([2, 1])

with col_input:
    st.markdown("### 📝 Input Your Text")
    
    input_method = st.radio(
        "✨ Choose input method:",
        ["✍️ Type/Paste Text", "📁 Upload File", "🎤 Voice Input (Coming Soon)"],
        horizontal=True
    )
    
    input_text = ""
    
    if input_method == "✍️ Type/Paste Text":
        input_text = st.text_area(
            "Enter text in any language:",
            height=150,
            placeholder="🌍 Type or paste your text here...\nExample: 'Your bank account needs verification.'",
            label_visibility="collapsed"
        )
    
    elif input_method == "📁 Upload File":
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'docx', 'pdf'],
            help="📄 Supports: .txt, .docx, .pdf"
        )
        if uploaded_file:
            # Your existing file processing code
            pass

with col_settings:
    st.markdown("### ⚙️ Output Settings")
    
    output_option = st.radio(
        "🎯 Select output:",
        ["🇮🇳 Tamil Only", "🇬🇧 English Only", "🌍 Both Languages"]
    )
    
    st.markdown("---")
    voice_option = st.checkbox("🔊 Add voice output", value=True)
    doc_option = st.checkbox("📄 Create downloadable file", value=True)
    
    process_btn = st.button(
        "✨ TRANSLATE NOW",
        type="primary",
        use_container_width=True,
        help="Click to translate and simplify your text"
    )

# ==================== PROCESSING ====================
if process_btn and input_text.strip():
    with st.spinner("🔄 Processing your request..."):
        # Your existing processing logic
        tamil_translation = ""
        simple_english = ""
        
        if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
            tamil_translation = translate_to_tamil(input_text)
        
        if output_option in ["🇬🇧 English Only", "🌍 Both Languages"]:
            simple_english = simplify_english(input_text)
        
        # Store in session
        st.session_state.current_output = {
            'tamil': tamil_translation,
            'simple_english': simple_english,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# ==================== RESULTS DISPLAY ====================
if st.session_state.current_output:
    st.markdown("---")
    st.markdown("## 📊 Translation Results")
    
    if output_option == "🌍 Both Languages":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("""
            <div class="lang-box tamil-box">
                <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.current_output['tamil']}**")
            
            if voice_option:
                audio_file = generate_tamil_audio(st.session_state.current_output['tamil'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    st.markdown("🎵 **Tamil Audio Ready**")
        
        with col_english:
            st.markdown("""
            <div class="lang-box english-box">
                <h3>🇬🇧 Simple English</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.current_output['simple_english']}**")
            
            if voice_option:
                audio_file = generate_english_audio(st.session_state.current_output['simple_english'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    st.markdown("🎵 **English Audio Ready**")
    
    else:  # Single language
        if output_option == "🇮🇳 Tamil Only":
            st.markdown("""
            <div class="lang-box tamil-box">
                <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
                <p>{}</p>
            </div>
            """.format(st.session_state.current_output['tamil']), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="lang-box english-box">
                <h3>🇬🇧 Simple English</h3>
                <p>{}</p>
            </div>
            """.format(st.session_state.current_output['simple_english']), unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>📊 Quick Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("🌐 Languages", "50+")
    with col_stat2:
        st.metric("🔊 Voice Outputs", "2")
    
    st.markdown("---")
    
    st.markdown("### 📖 Recent Translations")
    if st.session_state.translation_history:
        for item in reversed(st.session_state.translation_history[-3:]):
            emoji = "🇮🇳" if "Tamil" in item['output_option'] else "🇬🇧" if "English" in item['output_option'] else "🌍"
            st.markdown(f"{emoji} **{item['time']}**")
            st.caption(f"📝 {item['input'][:30]}...")
    else:
        st.info("📭 No translations yet")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Quick Examples")
    examples = {
        "🏦 Bank": "Your account needs verification.",
        "🏛️ Government": "Submit documents by 30th November.",
        "📚 Education": "Examination schedule is announced."
    }
    
    for icon, text in examples.items():
        if st.button(f"{icon} {text[:20]}...", use_container_width=True):
            st.session_state.example_text = text
            st.rerun()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🚀 <strong>Talk2Tamil</strong> - Bridging Language Gaps with Technology</p>
    <p>🌾 Made for Rural India | 🇮🇳 Proudly Indian | ❤️ Open Source</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        🔧 Built with: Streamlit • Python • Google Translate • gTTS
    </p>
</div>
""", unsafe_allow_html=True)
