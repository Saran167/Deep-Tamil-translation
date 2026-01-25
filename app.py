import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
from datetime import datetime
from PIL import Image
import os
import tempfile
import time
import json

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Voice Translation",
    page_icon="🎤",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E86C1;
        padding: 1rem;
        font-size: 2.5rem;
    }
    
    .language-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid;
    }
    
    .tamil-card {
        border-left-color: #FF6B6B;
        background: linear-gradient(135deg, #FFE8E8 0%, #FFCCCC 100%);
    }
    
    .english-card {
        border-left-color: #4ECDC4;
        background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
    }
    
    .voice-section {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #FF5252;
        margin: 2rem 0;
        text-align: center;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 0.5rem 0;
    }
    
    .record-btn {
        background: linear-gradient(90deg, #FF5252 0%, #FF1744 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        margin: 10px !important;
    }
    
    .stop-btn {
        background: linear-gradient(90deg, #00E676 0%, #00C853 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        margin: 10px !important;
    }
    
    .audio-player {
        width: 100%;
        border-radius: 10px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================
def translate_text(text, target_lang='ta'):
    """Translate text to target language"""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        return translated
    except:
        return text

def simplify_english(text):
    """Simplify English text"""
    replacements = {
        'artificial intelligence': 'smart computer systems',
        'machine learning': 'computers that learn',
        'agriculture': 'farming',
        'irrigation': 'water supply',
        'fertilizer': 'plant food',
        'subsidy': 'government help',
        'transaction': 'money transfer',
        'authentication': 'verification',
        'financial': 'money',
    }
    
    for complex_word, simple_word in replacements.items():
        text = text.replace(complex_word, simple_word)
    
    return text

def generate_audio(text, language='ta'):
    """Generate audio from text"""
    try:
        if language == 'ta':
            filename = "tamil_output.mp3"
            tts = gTTS(text=text, lang='ta', slow=False)
        else:
            filename = "english_output.mp3"
            tts = gTTS(text=text, lang='en', slow=False)
        
        tts.save(filename)
        return filename
    except:
        return None

def get_daily_tips(topic):
    """Get daily tips based on topic"""
    topic_lower = topic.lower()
    
    tips = {
        'agriculture': [
            "🌾 Sow seeds at right time for good yield",
            "💧 Use drip irrigation to save water",
            "🌱 Use organic fertilizers for soil health",
            "🐛 Follow natural pest control methods",
            "💰 Apply for government farming subsidies"
        ],
        'bank': [
            "🏦 Never share your OTP with anyone",
            "💳 Keep ATM PIN secret always",
            "📱 Use UPI apps safely with password",
            "📞 Report fraud to 1930 immediately",
            "💰 Check bank statements regularly"
        ],
        'ai': [
            "🤖 AI can automate repetitive tasks",
            "📱 Use voice assistants for daily help",
            "📊 AI analyzes data patterns",
            "🛡️ AI detects fraud and spam",
            "🎯 AI improves decision making"
        ]
    }
    
    if any(word in topic_lower for word in ['farm', 'crop', 'agriculture', 'irrigation']):
        return tips['agriculture'], 'agriculture'
    elif any(word in topic_lower for word in ['bank', 'money', 'otp', 'loan']):
        return tips['bank'], 'bank'
    elif any(word in topic_lower for word in ['ai', 'artificial', 'intelligence']):
        return tips['ai'], 'ai'
    else:
        return ["🌞 Learn something new every day!", "💡 Practice makes perfect!"], 'general'

# ==================== SESSION STATE ====================
if 'user_text' not in st.session_state:
    st.session_state.user_text = ""
if 'tamil_result' not in st.session_state:
    st.session_state.tamil_result = ""
if 'english_result' not in st.session_state:
    st.session_state.english_result = ""
if 'tamil_audio' not in st.session_state:
    st.session_state.tamil_audio = None
if 'english_audio' not in st.session_state:
    st.session_state.english_audio = None
if 'tips' not in st.session_state:
    st.session_state.tips = []
if 'topic' not in st.session_state:
    st.session_state.topic = ""

# ==================== HEADER ====================
st.markdown('<h1 class="main-title">🎤 Talk2Tamil - Voice Translation Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# ==================== VOICE INPUT SECTION ====================
st.markdown('<div class="voice-section">', unsafe_allow_html=True)
st.markdown("## 🎤 Voice Input Section")

# Simple voice input simulation
st.markdown("### Speak Your Message (Type what you would say)")

# Quick voice buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🌾 Agriculture", use_container_width=True):
        st.session_state.user_text = "Modern agriculture uses technology like AI for crop prediction and irrigation management."

with col2:
    if st.button("🏦 Banking", use_container_width=True):
        st.session_state.user_text = "Bank security requires never sharing OTP and using secure UPI apps."

with col3:
    if st.button("🤖 AI Tech", use_container_width=True):
        st.session_state.user_text = "Artificial intelligence helps analyze data and predict outcomes."

with col4:
    if st.button("🏥 Health", use_container_width=True):
        st.session_state.user_text = "Regular exercise and balanced diet maintain good health."

with col5:
    if st.button("📚 Education", use_container_width=True):
        st.session_state.user_text = "Education improves career opportunities through skill development."

# Text input area
user_input = st.text_area(
    "Type your spoken message here:",
    value=st.session_state.user_text,
    height=150,
    placeholder="Type what you want to say...\nExample: 'Artificial intelligence helps farmers predict crop diseases and improve harvest.'",
    key="voice_input"
)

if user_input != st.session_state.user_text:
    st.session_state.user_text = user_input

st.markdown('</div>', unsafe_allow_html=True)

# ==================== TRANSLATE BUTTON ====================
st.markdown("---")

if st.button("🚀 TRANSLATE NOW", type="primary", use_container_width=True):
    if st.session_state.user_text:
        with st.spinner("Translating..."):
            # Get translations
            st.session_state.tamil_result = translate_text(st.session_state.user_text, 'ta')
            st.session_state.english_result = simplify_english(st.session_state.user_text)
            
            # Generate audio
            st.session_state.tamil_audio = generate_audio(st.session_state.tamil_result, 'ta')
            st.session_state.english_audio = generate_audio(st.session_state.english_result, 'en')
            
            # Get tips
            st.session_state.tips, st.session_state.topic = get_daily_tips(st.session_state.user_text)
            
        st.success("✅ Translation complete!")
    else:
        st.warning("Please enter some text first!")

# ==================== TRANSLATION RESULTS ====================
if st.session_state.tamil_result or st.session_state.english_result:
    st.markdown("---")
    st.markdown("## 📊 Translation Results")
    
    # Create two columns for languages
    col_tamil, col_english = st.columns(2)
    
    with col_tamil:
        st.markdown('<div class="language-card tamil-card">', unsafe_allow_html=True)
        st.markdown("### 🇮🇳 Tamil Translation")
        
        if st.session_state.tamil_result:
            st.success(st.session_state.tamil_result)
            
            # Audio player for Tamil
            if st.session_state.tamil_audio and os.path.exists(st.session_state.tamil_audio):
                with open(st.session_state.tamil_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_english:
        st.markdown('<div class="language-card english-card">', unsafe_allow_html=True)
        st.markdown("### 🇬🇧 Simple English")
        
        if st.session_state.english_result:
            st.info(st.session_state.english_result)
            
            # Audio player for English
            if st.session_state.english_audio and os.path.exists(st.session_state.english_audio):
                with open(st.session_state.english_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== DAILY TIPS ====================
if st.session_state.tips:
    st.markdown("---")
    st.markdown("## 💡 Daily Useful Tips")
    
    st.success(f"📌 Topic: **{st.session_state.topic.upper()}**")
    
    # Display tips
    for i, tip in enumerate(st.session_state.tips[:5]):
        st.markdown(f'<div class="tip-box"><strong>Tip {i+1}:</strong> {tip}</div>', unsafe_allow_html=True)

# ==================== DOWNLOAD SECTION ====================
if st.session_state.user_text and st.session_state.tamil_result:
    st.markdown("---")
    st.markdown("## 📄 Download Results")
    
    # Create document content
    doc_content = f"""
    Talk2Tamil - Voice Translation Result
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Topic: {st.session_state.topic}
    
    Original Text:
    {st.session_state.user_text}
    
    Tamil Translation:
    {st.session_state.tamil_result}
    
    Simple English:
    {st.session_state.english_result}
    
    Daily Tips:
    {chr(10).join(f'- {tip}' for tip in st.session_state.tips)}
    """
    
    # Download button
    st.download_button(
        "📥 Download as Text File",
        doc_content,
        file_name=f"talk2tamil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 Quick Examples")
    
    examples = [
        ("🌾 Agriculture", "AI helps farmers predict crop diseases and improve harvest through data analysis."),
        ("🏦 Banking", "Never share your bank OTP with anyone for security and use secure UPI apps."),
        ("🤖 AI Technology", "Artificial intelligence analyzes data to help make better decisions in various fields."),
        ("🏥 Health Care", "Regular exercise and balanced diet are essential for maintaining good health."),
        ("📚 Education", "Continuous learning and skill development improve career opportunities.")
    ]
    
    for label, text in examples:
        if st.button(label, use_container_width=True):
            st.session_state.user_text = text
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.markdown("## ⚙️ Settings")
    auto_play = st.checkbox("Auto-play audio", value=True)
    show_tips = st.checkbox("Show daily tips", value=True)
    
    st.markdown("---")
    
    # Status
    st.markdown("## 📊 Status")
    if st.session_state.user_text:
        st.success("✅ Text ready")
        st.write(f"Words: {len(st.session_state.user_text.split())}")
    else:
        st.info("⏳ Waiting for input")
    
    st.markdown("---")
    
    # Help
    st.markdown("## ❓ How to Use")
    st.markdown("""
    1. **Type your message** in the voice section
    2. **Click TRANSLATE NOW**
    3. **View results** in both languages
    4. **Listen to audio** playback
    5. **Get daily tips**
    6. **Download results**
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("<center><small>🎤 Talk2Tamil - Making Information Accessible Through Voice Technology</small></center>", unsafe_allow_html=True)

# ==================== SIMPLE VOICE RECORDING JS ====================
# Simple JavaScript for basic voice recording simulation
st.markdown("""
<script>
// Simple voice recording simulation
function simulateVoiceRecording() {
    const textarea = document.querySelector('textarea[placeholder*="Type what you want to say"]');
    if (textarea) {
        // Sample phrases that appear as if being spoken
        const phrases = [
            "Artificial intelligence helps ",
            "Bank security requires ",
            "Agriculture improves with ",
            "Education opens ",
            "Health needs "
        ];
        
        let text = "";
        let i = 0;
        
        const typeInterval = setInterval(() => {
            if (i >= phrases.length) {
                clearInterval(typeInterval);
                return;
            }
            
            text += phrases[i] + "farmers, doctors, students. ";
            textarea.value = text;
            
            // Trigger input event for Streamlit
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            
            i++;
        }, 800);
    }
}

// Add a simple record button
const voiceSection = document.querySelector('.voice-section');
if (voiceSection) {
    const recordBtn = document.createElement('button');
    recordBtn.innerHTML = '🎤 Simulate Voice Input';
    recordBtn.style.cssText = 'background: #FF5252; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; margin: 10px auto; display: block;';
    recordBtn.onclick = simulateVoiceRecording;
    
    voiceSection.appendChild(recordBtn);
}
</script>
""", unsafe_allow_html=True)
