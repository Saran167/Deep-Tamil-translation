import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
from datetime import datetime
import os
import requests
import urllib.parse
import json

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Smart Translator",
    page_icon="🗣️",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .input-box {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .output-box {
        background-color: #ECFDF5;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .voice-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
        text-align: center;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================

def translate_to_tamil(text):
    """Translate text to Tamil"""
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def simplify_english(text):
    """Simplify English text"""
    simplification_dict = {
        'artificial intelligence': 'smart computer systems',
        'machine learning': 'computers that learn from data',
        'algorithms': 'step-by-step instructions',
        'computer science': 'computer studies',
        'software': 'computer programs',
        'programmed': 'given instructions',
        'data': 'information',
        'systems': 'setups',
        'performance': 'work quality',
        'applications': 'uses',
        'robotics': 'robot technology',
        'predictions': 'guesses',
        'understanding': 'knowing',
        'focuses on': 'works on',
        'creates': 'makes',
        'designed to': 'made to',
        'perform tasks': 'do jobs',
        'utilizes': 'uses',
        'improves': 'gets better',
        'makes decisions': 'chooses',
        'useful': 'helpful',
        'branch of': 'part of',
        'such as': 'like',
        'instead of': 'rather than',
        'over time': 'with time',
        'by using': 'using',
        'every single': 'each',
        'requires': 'needs',
        'verification': 'checking',
        'immediate': 'right away',
        'complex': 'complicated',
        'various': 'different',
        'capabilities': 'abilities',
        'significant': 'important',
        'approximately': 'about',
        'utilize': 'use',
        'terminate': 'end',
        'commence': 'start',
    }
    
    # Simple word replacement (case insensitive)
    import re
    simplified_text = text
    for complex_word, simple_word in simplification_dict.items():
        pattern = re.compile(re.escape(complex_word), re.IGNORECASE)
        simplified_text = pattern.sub(simple_word, simplified_text)
    
    # Break long sentences
    sentences = simplified_text.split('. ')
    short_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 15:
            # Split into two
            mid = len(words) // 2
            short_sentences.append(' '.join(words[:mid]) + '.')
            short_sentences.append(' '.join(words[mid:]))
        else:
            short_sentences.append(sentence)
    
    return '. '.join(short_sentences)

def generate_audio(text, language='ta'):
    """Generate audio from text"""
    try:
        if language == 'ta':
            filename = "tamil_audio.mp3"
            tts = gTTS(text=text, lang='ta', slow=False)
        else:
            filename = "english_audio.mp3"
            tts = gTTS(text=text, lang='en', slow=False)
        
        tts.save(filename)
        return filename
    except Exception as e:
        # Fallback to Google TTS API
        try:
            text_encoded = urllib.parse.quote(text)
            if language == 'ta':
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=ta&client=tw-ob"
                filename = "tamil_audio.mp3"
            else:
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=en&client=tw-ob"
                filename = "english_audio.mp3"
            
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
        except:
            pass
        return None

# ==================== BROWSER VOICE INPUT (JavaScript) ====================
def voice_input_script():
    """JavaScript for browser voice recognition"""
    return """
    <script>
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        // Set language based on selection
        function setLanguage(lang) {
            if (lang === 'ta') {
                recognition.lang = 'ta-IN'; // Tamil India
            } else {
                recognition.lang = 'en-IN'; // English India
            }
        }
        
        // Start recording
        window.startVoiceRecording = function(lang) {
            setLanguage(lang);
            recognition.start();
            
            // Update status
            document.getElementById('status').innerHTML = '🎤 Listening... Speak now!';
            document.getElementById('status').style.color = 'red';
        };
        
        // Handle result
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('voice-input').value = transcript;
            document.getElementById('status').innerHTML = '✅ Voice captured!';
            document.getElementById('status').style.color = 'green';
            
            // Auto-submit the form
            document.getElementById('voice-form').submit();
        };
        
        // Handle errors
        recognition.onerror = function(event) {
            document.getElementById('status').innerHTML = '❌ Error: ' + event.error;
            document.getElementById('status').style.color = 'red';
        };
        
        recognition.onend = function() {
            document.getElementById('status').innerHTML = '🎤 Click button to speak again';
            document.getElementById('status').style.color = 'blue';
        };
    } else {
        document.getElementById('status').innerHTML = '❌ Your browser does not support speech recognition. Try Chrome.';
        document.getElementById('status').style.color = 'red';
    }
    </script>
    
    <form id="voice-form">
        <input type="hidden" id="voice-input" name="voice_text">
    </form>
    
    <div id="status" style="margin: 10px 0; font-weight: bold; color: blue;">
        🎤 Ready to speak
    </div>
    """

# ==================== MAIN APP ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>🗣️ Talk2Tamil: Smart Translator</h1>
    <p>🎤 Voice Input | 🌍 Any Language → 🇮🇳 Tamil OR 🇬🇧 Simple English | 🔊 Voice Output</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_translation' not in st.session_state:
    st.session_state.current_translation = None
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""

# Check for voice input from form
if 'voice_text' in st.query_params:
    st.session_state.voice_text = st.query_params['voice_text']

# ==================== INPUT SECTION ====================
st.markdown("<div class='input-box'><h3>📝 Input Your Text</h3></div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Input method selection
    input_method = st.radio(
        "✨ Choose input method:",
        ["✍️ Type/Paste Text", "🎤 Voice Input (Speak)", "📁 Upload Image (Coming Soon)"],
        horizontal=True
    )
    
    # Main input area
    if input_method == "✍️ Type/Paste Text":
        input_text = st.text_area(
            "Enter text in any language:",
            height=200,
            placeholder="Type or paste your text here...\nExample: 'Your bank account requires immediate verification.'",
            key="text_input"
        )
    
    elif input_method == "🎤 Voice Input (Speak)":
        st.markdown("""
        <div class="voice-box">
            <h4>🎙️ Speak in Tamil or English</h4>
            <p>1. Select language below<br>
            2. Click "Start Speaking"<br>
            3. Speak clearly<br>
            4. Your speech will appear here</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice language selection
        voice_lang = st.radio(
            "Speak in:",
            ["தமிழ் (Tamil)", "English"],
            horizontal=True
        )
        
        # Voice buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎤 Start Speaking", use_container_width=True):
                # This would trigger JavaScript
                st.info("Voice recording would start here. On local machine, this works!")
        
        with col_btn2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.success("Voice recorded!")
        
        # Show voice input area
        voice_input_text = st.text_area(
            "🎤 Your voice input will appear here:",
            value=st.session_state.voice_text,
            height=150,
            placeholder="Speak and your words will appear here...",
            key="voice_input_display"
        )
        
        input_text = voice_input_text
        
        # Add JavaScript for voice input
        st.components.v1.html(f"""
        <div style="padding: 10px;">
            {voice_input_script()}
            <button onclick="startVoiceRecording('{'ta' if voice_lang.startswith('தமிழ்') else 'en'}')" 
                style="background: linear-gradient(90deg, #EF4444 0%, #DC2626 100%); 
                       color: white; border: none; padding: 12px 24px; 
                       border-radius: 8px; font-size: 16px; cursor: pointer; 
                       margin: 10px 0;">
                🎤 Start Speaking in {voice_lang}
            </button>
        </div>
        """, height=200)
    
    else:  # Image upload
        st.info("📸 Image upload feature coming soon!")
        st.image("https://via.placeholder.com/600x200/667eea/ffffff?text=Upload+Image+of+Text", 
                caption="Upload image of text to extract")
        input_text = st.text_area(
            "Or type text here:",
            height=150,
            placeholder="For now, type your text here...",
            key="alt_input"
        )

with col2:
    st.markdown("<div class='input-box'><h3>⚙️ Output Settings</h3></div>", unsafe_allow_html=True)
    
    # Output language selection
    output_option = st.radio(
        "🎯 Select output language:",
        ["🇮🇳 Tamil Only", "🇬🇧 Simple English Only", "🌍 Both Languages"],
        key="output_option"
    )
    
    st.markdown("---")
    
    # Voice output option
    voice_output = st.checkbox("🔊 Generate voice output", value=True, key="voice_output")
    
    st.markdown("---")
    
    # Process button
    process_btn = st.button(
        "✨ TRANSLATE & SIMPLIFY",
        type="primary",
        use_container_width=True,
        key="process_btn"
    )

# ==================== PROCESSING ====================
if process_btn:
    # Get the right input text
    if input_method == "✍️ Type/Paste Text":
        text_to_process = st.session_state.text_input
    elif input_method == "🎤 Voice Input (Speak)":
        text_to_process = st.session_state.voice_input_display
    else:
        text_to_process = st.session_state.alt_input if 'alt_input' in st.session_state else ""
    
    if text_to_process and text_to_process.strip():
        with st.spinner("🔄 Processing..."):
            # Get translations
            tamil_text = ""
            english_text = ""
            
            if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
                tamil_text = translate_to_tamil(text_to_process)
            
            if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
                english_text = simplify_english(text_to_process)
            
            # Store in session
            st.session_state.current_translation = {
                'original': text_to_process,
                'tamil': tamil_text,
                'english': english_text,
                'output_option': output_option
            }
    else:
        st.warning("⚠️ Please enter some text to translate.")

# ==================== OUTPUT SECTION ====================
if st.session_state.current_translation:
    st.markdown("---")
    st.markdown("<div class='output-box'><h3>📊 Translation Results</h3></div>", unsafe_allow_html=True)
    
    # Show original input
    with st.expander("📝 View Original Input"):
        st.write(st.session_state.current_translation['original'])
    
    output_option = st.session_state.current_translation['output_option']
    
    if output_option == "🌍 Both Languages":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("### 🇮🇳 தமிழ் மொழிபெயர்ப்பு")
            tamil_text = st.session_state.current_translation['tamil']
            st.success(tamil_text)
            
            if voice_output and tamil_text:
                if st.button("🔊 Play Tamil Audio", key="play_tamil"):
                    audio_file = generate_audio(tamil_text, 'ta')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        st.success("✅ Tamil audio playing")
        
        with col_english:
            st.markdown("### 🇬🇧 Simple English")
            english_text = st.session_state.current_translation['english']
            
            # Show simplification comparison
            original = st.session_state.current_translation['original']
            if english_text != original:
                st.info("**Simplified from:** " + original[:100] + "...")
            
            st.success(english_text)
            
            if voice_output and english_text:
                if st.button("🔊 Play English Audio", key="play_english"):
                    audio_file = generate_audio(english_text, 'en')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        st.success("✅ English audio playing")
    
    elif output_option == "🇮🇳 Tamil Only":
        st.markdown("### 🇮🇳 Tamil Translation")
        tamil_text = st.session_state.current_translation['tamil']
        st.success(tamil_text)
        
        if voice_output and tamil_text:
            if st.button("🔊 Play Tamil Audio"):
                audio_file = generate_audio(tamil_text, 'ta')
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
    
    else:  # Simple English Only
        st.markdown("### 🇬🇧 Simplified English")
        english_text = st.session_state.current_translation['english']
        
        # Show what was simplified
        original = st.session_state.current_translation['original']
        if english_text != original:
            col_orig, col_simp = st.columns(2)
            with col_orig:
                st.markdown("**Original:**")
                st.info(original[:200] + "..." if len(original) > 200 else original)
            with col_simp:
                st.markdown("**Simplified:**")
                st.success(english_text[:200] + "..." if len(english_text) > 200 else english_text)
        else:
            st.success(english_text)
        
        if voice_output and english_text:
            if st.button("🔊 Play English Audio"):
                audio_file = generate_audio(english_text, 'en')
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📋 Quick Examples")
    
    examples = {
        "🏦 Bank Alert": "Your account has been temporarily suspended. Please verify your identity immediately.",
        "📱 OTP Scam": "Your OTP is 123456. Do not share with anyone.",
        "🎓 Education": "Artificial Intelligence is transforming the educational landscape.",
        "🏥 Health": "Regular exercise and balanced diet are essential for maintaining good health.",
    }
    
    for title, text in examples.items():
        if st.button(f"{title}", use_container_width=True):
            # Set the text in the main input
            if 'text_input' in st.session_state:
                st.session_state.text_input = text
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("## 💡 Tips")
    st.markdown("""
    **For best results:**
    - Speak clearly for voice input
    - Use complete sentences
    - Tamil voice works best in Chrome
    
    **Simplification:**
    - Complex words become simple
    - Long sentences are shortened
    - Technical terms are explained
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <p>🚀 <strong>Talk2Tamil</strong> - Smart Translation Assistant</p>
    <p>🎤 Voice Input | 🌍 Any Language → 🇮🇳 Tamil | 🇬🇧 Simple English | 🔊 Voice Output</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit • Google Translate • gTTS</p>
</div>
""", unsafe_allow_html=True)
