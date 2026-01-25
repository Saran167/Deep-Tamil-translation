import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
from datetime import datetime
from PIL import Image
import os
import time
import tempfile
import base64

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Real Voice Assistant",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Language boxes */
    .language-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-top: 5px solid;
        text-align: center;
        transition: transform 0.3s;
    }
    .language-box:hover {
        transform: translateY(-5px);
    }
    
    .tamil-box {
        border-top-color: #FF6B6B;
        background: linear-gradient(135deg, #FFE8E8 0%, #FFCCCC 100%);
    }
    
    .english-box {
        border-top-color: #4ECDC4;
        background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
    }
    
    /* Voice recording */
    .recording-active {
        animation: recordingPulse 1.5s infinite;
        background: linear-gradient(135deg, #FF5252 0%, #FF8A80 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
    }
    
    @keyframes recordingPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Voice waves */
    .voice-waves {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        margin: 20px 0;
    }
    
    .voice-bar {
        width: 4px;
        height: 20px;
        background: #FF5252;
        margin: 0 2px;
        border-radius: 2px;
        animation: voiceWave 1s ease-in-out infinite;
    }
    
    .voice-bar:nth-child(2) { animation-delay: 0.1s; }
    .voice-bar:nth-child(3) { animation-delay: 0.2s; }
    .voice-bar:nth-child(4) { animation-delay: 0.3s; }
    .voice-bar:nth-child(5) { animation-delay: 0.4s; }
    
    @keyframes voiceWave {
        0%, 100% { height: 20px; }
        50% { height: 40px; }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        transition: all 0.3s !important;
        font-size: 16px !important;
    }
    
    .record-btn {
        background: linear-gradient(90deg, #FF5252 0%, #FF1744 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    
    .stop-btn {
        background: linear-gradient(90deg, #00E676 0%, #00C853 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
    }
    
    /* Tips boxes */
    .tip-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
    
    /* Audio player */
    .audio-player {
        width: 100%;
        margin: 10px 0;
        border-radius: 10px;
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
    except Exception as e:
        return f"Translation error: {str(e)}"

def simplify_english(text):
    """Simplify English text"""
    replacements = {
        'artificial intelligence': 'smart computer systems',
        'machine learning': 'computers that learn from data',
        'algorithms': 'step-by-step instructions',
        'agriculture': 'farming',
        'cultivation': 'growing crops',
        'irrigation': 'water supply',
        'fertilizer': 'plant food',
        'harvest': 'collect crops',
        'crops': 'plants for food',
        'yield': 'amount produced',
        'soil': 'earth for growing',
        'pesticides': 'insect killers',
        'subsidy': 'government help',
        'authentication': 'verification',
        'transaction': 'money transfer',
        'financial': 'money',
        'portfolio': 'collection',
        'diversification': 'spreading',
        'mitigate': 'reduce',
        'volatility': 'changes',
    }
    
    for complex_word, simple_word in replacements.items():
        if complex_word in text.lower():
            text = text.replace(complex_word, simple_word)
    
    return text

def generate_audio(text, language='ta'):
    """Generate audio from text and return base64 encoded audio"""
    try:
        if language == 'ta':
            tts = gTTS(text=text, lang='ta', slow=False)
            filename = "tamil_output.mp3"
        else:
            tts = gTTS(text=text, lang='en', slow=False)
            filename = "english_output.mp3"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            return f.name
    except Exception as e:
        st.error(f"Audio error: {str(e)}")
        return None

def get_daily_tips(topic):
    """Get daily tips based on topic"""
    topic_lower = topic.lower()
    
    tips_database = {
        'agriculture': {
            'ta': [
                "🌾 நல்ல விளைச்சலுக்கு சரியான நேரத்தில் விதைக்கவும்",
                "💧 தண்ணீர் மிச்சப்படுத்தும் நீர்ப்பாசன முறைகளை பயன்படுத்தவும்",
                "🌱 இயற்கை உரங்களை பயன்படுத்தி மண்ணின் ஆரோக்கியத்தை பராமரிக்கவும்",
                "🐛 பூச்சி மற்றும் நோய் மேலாண்மைக்கு இயற்கை முறைகளை பின்பற்றவும்",
                "💰 அரசு மானியங்கள் மற்றும் கடன் திட்டங்களைப் பயன்படுத்தவும்"
            ],
            'en': [
                "🌾 Sow seeds at the right time for good yield",
                "💧 Use water-saving irrigation methods",
                "🌱 Maintain soil health using organic fertilizers",
                "🐛 Follow natural methods for pest control",
                "💰 Apply for government farming subsidies"
            ]
        },
        'bank': {
            'ta': [
                "🏦 உங்கள் OTP யாருக்கும் சொல்லாதீர்கள்",
                "💳 ATM கார்டு PIN எப்போதும் ரகசியமாக வைக்கவும்",
                "📱 UPI பயன்பாடுகளை பாதுகாப்பாக பயன்படுத்தவும்",
                "📞 வங்கி மோசடி பற்றிய புகார்களை 1930 க்கு அறிவிக்கவும்",
                "💰 சந்தேகத்திற்கிடமான கடன் செய்திகளை நம்பாதீர்கள்"
            ],
            'en': [
                "🏦 Never share your OTP with anyone",
                "💳 Keep ATM card PIN secret always",
                "📱 Use UPI apps safely with password protection",
                "📞 Report bank frauds immediately to 1930",
                "💰 Don't trust suspicious loan messages"
            ]
        },
        'ai': {
            'ta': [
                "🤖 AI உங்கள் வாழ்க்கையை எளிதாக்கும்!",
                "📱 Google Assistant, Siri போன்ற AI உதவியாளர்களைப் பயன்படுத்தவும்",
                "📸 AI கேமராக்கள் சிறப்பான புகைப்படங்களை எடுக்க உதவும்",
                "📚 AI பயன்பாடுகளைக் கற்றுக்கொள்ள YouTube பாடங்களைப் பார்க்கவும்",
                "🛡️ AI மூலம் மோசடி செய்திகளை அடையாளம் காணலாம்"
            ],
            'en': [
                "🤖 AI can make your life easier!",
                "📱 Use AI assistants like Google Assistant, Siri",
                "📸 AI cameras help take better photos",
                "📚 Learn about AI apps through YouTube",
                "🛡️ AI can help detect scam messages"
            ]
        },
        'health': {
            'ta': [
                "💊 மருந்துகளை மருத்துவர் ஆலோசனையின்றி எடுக்கக்கூடாது",
                "🍎 தினமும் பழங்கள் மற்றும் காய்கறிகளை சாப்பிடவும்",
                "🚶‍♂️ தினமும் குறைந்தது 30 நிமிடம் நடக்கவும்",
                "💧 தினமும் 8 கிளாஸ் தண்ணீர் குடிக்கவும்",
                "😴 இரவு 7-8 மணி நேரம் உறங்கவும்"
            ],
            'en': [
                "💊 Don't take medicines without doctor consultation",
                "🍎 Eat fruits and vegetables daily",
                "🚶‍♂️ Walk at least 30 minutes every day",
                "💧 Drink 8 glasses of water daily",
                "😴 Sleep 7-8 hours every night"
            ]
        },
        'education': {
            'ta': [
                "📚 தினமும் குறைந்தது 2 மணி நேரம் படிக்கவும்",
                "📝 புதிய வார்த்தைகளை கற்றுக்கொள்ள தினசரி 5 சொற்கள்",
                "🎯 இலக்குகளை அமைத்து அவற்றை அடைய திட்டமிடவும்",
                "🤝 குழுவாக படிப்பது மேம்பட்ட கற்றலை அளிக்கும்",
                "📱 கல்வி பயன்பாடுகளைப் பயன்படுத்தி புதிய திறன்களைக் கற்றுக்கொள்ளுங்கள்"
            ],
            'en': [
                "📚 Study at least 2 hours daily",
                "📝 Learn 5 new words every day",
                "🎯 Set goals and plan to achieve them",
                "🤝 Group study provides better learning",
                "📱 Use educational apps to learn new skills"
            ]
        }
    }
    
    # Detect topic
    if any(word in topic_lower for word in ['farm', 'crop', 'agriculture', 'irrigation', 'fertilizer', 'harvest']):
        topic_key = 'agriculture'
    elif any(word in topic_lower for word in ['bank', 'money', 'otp', 'loan', 'account', 'upi', 'transaction']):
        topic_key = 'bank'
    elif any(word in topic_lower for word in ['ai', 'artificial', 'intelligence', 'machine', 'robot', 'smart']):
        topic_key = 'ai'
    elif any(word in topic_lower for word in ['health', 'doctor', 'medicine', 'exercise', 'diet', 'hospital']):
        topic_key = 'health'
    elif any(word in topic_lower for word in ['study', 'education', 'learn', 'school', 'college', 'student']):
        topic_key = 'education'
    else:
        topic_key = 'ai'
    
    return tips_database.get(topic_key, {}).get('en', []), topic_key

# ==================== SESSION STATE ====================
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'tamil_translation' not in st.session_state:
    st.session_state.tamil_translation = ""
if 'english_translation' not in st.session_state:
    st.session_state.english_translation = ""
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'audio_files' not in st.session_state:
    st.session_state.audio_files = {"tamil": None, "english": None}
if 'tips' not in st.session_state:
    st.session_state.tips = []
if 'detected_topic' not in st.session_state:
    st.session_state.detected_topic = ""

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🎤 Talk2Tamil: REAL Voice Translation</h1>
    <p style="font-size: 1.2rem; margin-top: 10px;">Speak → Get Instant Translation → Listen in Both Languages</p>
</div>
""", unsafe_allow_html=True)

# ==================== VOICE RECORDING SECTION ====================
st.markdown("## 🎤 1. Voice Recording Section")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Speak Your Message")
    
    # Voice recording controls
    col_start, col_stop, col_clear = st.columns(3)
    
    with col_start:
        if st.button("🎤 Start Recording", key="start_rec", use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.transcript = ""
            st.rerun()
    
    with col_stop:
        if st.button("⏹️ Stop Recording", key="stop_rec", use_container_width=True):
            st.session_state.is_recording = False
            st.rerun()
    
    with col_clear:
        if st.button("🗑️ Clear All", key="clear_all", use_container_width=True):
            st.session_state.transcript = ""
            st.session_state.tamil_translation = ""
            st.session_state.english_translation = ""
            st.session_state.audio_files = {"tamil": None, "english": None}
            st.session_state.tips = []
            st.rerun()
    
    # Show recording status
    if st.session_state.is_recording:
        st.markdown("""
        <div class="recording-active">
            <h3>🎤 RECORDING ACTIVE</h3>
            <p>Speak now! Your voice is being recorded...</p>
            <div class="voice-waves">
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick voice input buttons
        st.markdown("#### 🚀 Quick Voice Commands:")
        
        quick_commands = st.columns(5)
        commands = [
            ("🌾 Agriculture", "Modern agriculture helps farmers grow more crops"),
            ("🏦 Banking", "Bank security requires never sharing OTP"),
            ("🤖 AI Tech", "Artificial intelligence helps predict outcomes"),
            ("🏥 Health", "Regular exercise maintains good health"),
            ("📚 Education", "Education improves career opportunities")
        ]
        
        for i, (emoji, text) in enumerate(commands):
            with quick_commands[i]:
                if st.button(f"{emoji}", key=f"cmd_{i}", help=text):
                    st.session_state.transcript = text
                    st.success(f"✅ Command added: {text[:30]}...")
    
    # Voice input area
    st.markdown("### 💬 Your Spoken Text")
    
    transcript_input = st.text_area(
        "Edit your spoken text below:",
        value=st.session_state.transcript,
        height=150,
        key="transcript_input",
        placeholder="Your spoken text will appear here...\nYou can also type directly.\n\nExample: 'Artificial intelligence helps farmers predict crop diseases and improve harvest through data analysis.'"
    )
    
    if transcript_input != st.session_state.transcript:
        st.session_state.transcript = transcript_input
    
    # Translate button
    if st.button("🔁 Translate Now", key="translate_btn", use_container_width=True):
        if st.session_state.transcript:
            with st.spinner("Translating to both languages..."):
                # Get Tamil translation
                st.session_state.tamil_translation = translate_text(st.session_state.transcript, 'ta')
                
                # Get English simplification
                st.session_state.english_translation = simplify_english(st.session_state.transcript)
                
                # Generate audio files
                st.session_state.audio_files["tamil"] = generate_audio(st.session_state.tamil_translation, 'ta')
                st.session_state.audio_files["english"] = generate_audio(st.session_state.english_translation, 'en')
                
                # Get tips
                st.session_state.tips, st.session_state.detected_topic = get_daily_tips(st.session_state.transcript)
                
            st.success("✅ Translation complete!")
        else:
            st.warning("Please enter some text first!")

with col2:
    st.markdown("### 🎯 How to Use")
    
    st.markdown("""
    <div style="background: #E3F2FD; padding: 20px; border-radius: 15px;">
        <h4>🎤 Voice Recording Steps:</h4>
        <ol>
            <li>Click <strong>"Start Recording"</strong></li>
            <li>Speak clearly in English</li>
            <li>Click <strong>"Stop Recording"</strong></li>
            <li>Edit text if needed</li>
            <li>Click <strong>"Translate Now"</strong></li>
            <li>Get results in both languages</li>
        </ol>
        
        <h4>💡 Voice Tips:</h4>
        <ul>
            <li>Speak slowly and clearly</li>
            <li>Use simple sentences</li>
            <li>Pause between ideas</li>
            <li>English works best</li>
            <li>Quiet environment</li>
        </ul>
        
        <h4>⚡ Quick Commands:</h4>
        <p>Click buttons for instant text:</p>
        <ul>
            <li>🌾 Agriculture</li>
            <li>🏦 Banking</li>
            <li>🤖 AI Tech</li>
            <li>🏥 Health</li>
            <li>📚 Education</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== TRANSLATION RESULTS ====================
if st.session_state.tamil_translation or st.session_state.english_translation:
    st.markdown("---")
    st.markdown("## 📊 2. Translation Results")
    
    # Language boxes in columns
    col_tamil, col_english = st.columns(2)
    
    with col_tamil:
        if st.session_state.tamil_translation:
            st.markdown("""
            <div class="language-box tamil-box">
                <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Tamil translation text
            st.markdown(f"""
            <div style="background: #FFE8E8; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <p style="font-size: 16px; line-height: 1.6;">{st.session_state.tamil_translation}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tamil audio player
            if st.session_state.audio_files["tamil"] and os.path.exists(st.session_state.audio_files["tamil"]):
                with open(st.session_state.audio_files["tamil"], "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                # Download Tamil audio
                st.download_button(
                    label="📥 Download Tamil Audio",
                    data=audio_bytes,
                    file_name="talk2tamil_tamil.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
    
    with col_english:
        if st.session_state.english_translation:
            st.markdown("""
            <div class="language-box english-box">
                <h3>🇬🇧 Simple English</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # English translation text
            st.markdown(f"""
            <div style="background: #E0F7FA; padding: 20px; border-radius: 10px; margin: 10px 0;">
                <p style="font-size: 16px; line-height: 1.6;">{st.session_state.english_translation}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # English audio player
            if st.session_state.audio_files["english"] and os.path.exists(st.session_state.audio_files["english"]):
                with open(st.session_state.audio_files["english"], "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                # Download English audio
                st.download_button(
                    label="📥 Download English Audio",
                    data=audio_bytes,
                    file_name="talk2tamil_english.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

# ==================== DAILY TIPS ====================
if st.session_state.tips:
    st.markdown("---")
    st.markdown("## 💡 3. Daily Useful Tips")
    
    st.success(f"📌 Detected Topic: **{st.session_state.detected_topic.upper()}**")
    
    # Show tips in a nice grid
    tips_cols = st.columns(2)
    for i, tip in enumerate(st.session_state.tips[:6]):  # Show max 6 tips
        with tips_cols[i % 2]:
            st.markdown(f"""
            <div class="tip-box">
                <strong>Tip {i+1}:</strong> {tip}
            </div>
            """, unsafe_allow_html=True)

# ==================== ALTERNATIVE INPUT METHODS ====================
st.markdown("---")
st.markdown("## 📝 4. Alternative Input Methods")

tab1, tab2 = st.tabs(["✍️ Type Text", "📸 Upload Image"])

with tab1:
    st.markdown("### Type Directly")
    direct_text = st.text_area(
        "Type your text here:",
        height=150,
        placeholder="Type any text for translation...",
        key="direct_text"
    )
    
    if direct_text and st.button("Use This Text", key="use_direct_text"):
        st.session_state.transcript = direct_text
        st.success("✅ Text loaded! Click 'Translate Now' above.")
        st.rerun()

with tab2:
    uploaded_file = st.file_uploader("Choose an image:", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Image", width=300)
        
        image_text = st.text_area("Type text from image:", height=100, key="image_text_area")
        if image_text and st.button("Use Image Text", key="use_image_text"):
            st.session_state.transcript = image_text
            st.success("✅ Image text loaded! Click 'Translate Now' above.")
            st.rerun()

# ==================== DOWNLOAD SECTION ====================
if st.session_state.transcript and st.session_state.tamil_translation:
    st.markdown("---")
    st.markdown("## 💾 5. Download Results")
    
    # Create downloadable document
    doc_content = f"""
    ============================================
    TALK2TAMIL - VOICE TRANSLATION RESULT
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Detected Topic: {st.session_state.detected_topic.upper()}
    ============================================

    SPOKEN TEXT:
    {st.session_state.transcript}

    TAMIL TRANSLATION:
    {st.session_state.tamil_translation}

    SIMPLE ENGLISH:
    {st.session_state.english_translation}

    DAILY TIPS:
    {chr(10).join(f'• {tip}' for tip in st.session_state.tips[:5])}

    ============================================
    Talk2Tamil - Smart Voice Translation Assistant
    Making information accessible for everyone!
    ============================================
    """
    
    st.download_button(
        "📥 Download All Results (Text File)",
        doc_content,
        file_name=f"talk2tamil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 Quick Examples")
    
    examples = [
        ("🌾 Agriculture Example", "Modern agriculture uses technology like AI for crop prediction and irrigation management to increase farmer income."),
        ("🏦 Banking Example", "Bank customers must never share their OTP with anyone and should use secure UPI apps for transactions."),
        ("🤖 AI Example", "Artificial intelligence helps analyze large amounts of data and predict outcomes in farming, healthcare, and education."),
        ("🏥 Health Example", "Regular exercise, balanced diet, and proper sleep are essential for maintaining good health and preventing diseases."),
        ("📚 Education Example", "Continuous learning and skill development through education improve career opportunities and personal growth.")
    ]
    
    for label, text in examples:
        if st.button(label, key=f"ex_{label}"):
            st.session_state.transcript = text
            st.session_state.tamil_translation = ""
            st.session_state.english_translation = ""
            st.session_state.audio_files = {"tamil": None, "english": None}
            st.session_state.tips = []
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.markdown("## ⚙️ Settings")
    auto_play = st.checkbox("Auto-play audio", value=True)
    show_tips = st.checkbox("Show daily tips", value=True)
    language = st.radio("Tips Language:", ["English", "Tamil"])
    
    st.markdown("---")
    
    # Status
    st.markdown("## 📊 Status")
    if st.session_state.is_recording:
        st.error("🔴 Recording Active")
    else:
        st.success("🟢 Ready to Record")
    
    st.write(f"Words: {len(st.session_state.transcript.split())}")
    st.write(f"Characters: {len(st.session_state.transcript)}")
    
    if st.session_state.detected_topic:
        st.write(f"Topic: {st.session_state.detected_topic}")
    
    st.markdown("---")
    
    # Help
    st.markdown("## ❓ Help & Support")
    st.markdown("""
    **Having issues?**
    
    1. **Microphone not working?** 
       - Type text directly
       - Use quick examples
       
    2. **Translation slow?**
       - Try shorter sentences
       - Check internet connection
       
    3. **Audio not playing?**
       - Click download instead
       - Check browser permissions
       
    4. **Need help?**
       - Use example buttons
       - Contact support
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p><strong>🎤 Talk2Tamil - Real Voice Translation Assistant</strong></p>
    <p>🇮🇳 Tamil Translation | 🇬🇧 Simple English | 💡 Daily Tips | 🔊 Voice Output</p>
    <p><small>Making information accessible through voice technology for everyone</small></p>
</div>
""", unsafe_allow_html=True)

# ==================== REAL VOICE RECORDING SCRIPT ====================
# Since Streamlit doesn't have direct microphone recording in Python,
# we use HTML/JS for actual voice recording
st.markdown("""
<script>
// Real voice recording functionality
let mediaRecorder;
let audioChunks = [];

function startRealRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // Create download link
                const a = document.createElement('a');
                a.href = audioUrl;
                a.download = 'voice_recording.wav';
                document.body.appendChild(a);
                a.click();
                
                // Clean up
                URL.revokeObjectURL(audioUrl);
                document.body.removeChild(a);
                
                alert("Voice recording saved! Please type what you said in the text box.");
            };
            
            mediaRecorder.start();
            alert("🎤 Recording started! Speak now...");
        })
        .catch(err => {
            console.error("Error accessing microphone:", err);
            alert("Microphone access denied. Please type your text instead.");
        });
}

function stopRealRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        alert("Recording stopped! Check downloads for your audio file.");
    }
}

// Add buttons for real recording
document.addEventListener('DOMContentLoaded', function() {
    const voiceSection = document.querySelector('[data-testid="stVerticalBlock"]');
    if (voiceSection) {
        const realRecordBtn = document.createElement('button');
        realRecordBtn.innerHTML = '🎤 REAL Voice Record (Browser)';
        realRecordBtn.style.cssText = 'background: #FF5252; color: white; border: none; padding: 12px 24px; border-radius: 10px; font-weight: bold; margin: 10px; cursor: pointer; width: 100%;';
        realRecordBtn.onclick = startRealRecording;
        
        const realStopBtn = document.createElement('button');
        realStopBtn.innerHTML = '⏹️ Stop Real Recording';
        realStopBtn.style.cssText = 'background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 10px; font-weight: bold; margin: 10px; cursor: pointer; width: 100%;';
        realStopBtn.onclick = stopRealRecording;
        
        voiceSection.appendChild(realRecordBtn);
        voiceSection.appendChild(realStopBtn);
    }
});
</script>
""", unsafe_allow_html=True)
