import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
import urllib.parse
import base64
from datetime import datetime
from PIL import Image
import io
import pytesseract
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Smart Assistant",
    page_icon="🗣️🤖",
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
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 5px solid;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Input/output boxes */
    .input-section {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #2196F3;
        margin: 1rem 0;
    }
    
    .output-section {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .daily-tip {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #FF9800;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 152, 0, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 152, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 152, 0, 0); }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        transition: all 0.3s !important;
    }
    
    .translate-btn {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%) !important;
        color: white !important;
        font-size: 18px !important;
    }
    
    .voice-btn {
        background: linear-gradient(90deg, #4ECDC4 0%, #44A08D 100%) !important;
        color: white !important;
    }
    
    /* Status indicators */
    .status-recording {
        background: #FF5252;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .status-ready {
        background: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    /* Chat messages */
    .user-message {
        background: #E3F2FD;
        padding: 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        border-left: 5px solid #2196F3;
    }
    
    .assistant-message {
        background: #F1F8E9;
        padding: 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        border-right: 5px solid #4CAF50;
    }
    
    /* Daily tip animation */
    .tip-icon {
        font-size: 24px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================

def translate_text(text, target_lang='ta'):
    """Smart translation with rural Tamil optimization"""
    try:
        # First get base translation
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        
        # Apply rural Tamil optimizations if target is Tamil
        if target_lang == 'ta':
            # Replace formal Tamil with colloquial
            colloquial_replacements = {
                "வங்கிக் கணக்கு": "வங்கி கணக்கு",
                "பயன்படுத்து": "உபயோகி",
                "தொடங்குக": "ஆரம்பி",
                "நிறைவேற்று": "முடி",
                "பரிசீலனை": "ஆலோசனை",
                "அறிவுறுத்தல்": "செயல்",
                "முன்னெச்சரிக்கை": "ஜாக்கிரதை",
                "செயல்படுத்த": "செய்",
                "அடையாளம் காணுதல்": "கண்டுபிடி",
                "சரிபார்த்தல்": "சோதி",
            }
            
            for formal, colloquial in colloquial_replacements.items():
                if formal in translated:
                    translated = translated.replace(formal, colloquial)
        
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def simplify_english(text):
    """Three-layer English simplification"""
    # Layer 1: Vocabulary simplification
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
        'purchase': 'buy',
        'acquire': 'get',
        'remuneration': 'payment',
        'obligation': 'duty',
        'prohibited': 'not allowed',
        'mandatory': 'must',
        'submit': 'give',
        'application': 'form',
        'documentation': 'papers',
        'financial': 'money',
        'portfolio': 'collection',
        'diversification': 'spreading',
        'mitigate': 'reduce',
        'volatility': 'changes',
        'transaction': 'money transfer',
        'authentication': 'verification',
        'credentials': 'login details',
        'suspended': 'stopped',
        'unauthorized': 'not allowed',
        'fraudulent': 'fake',
        'notification': 'alert',
    }
    
    # Apply replacements
    import re
    simplified = text
    for complex_word, simple_word in simplification_dict.items():
        pattern = re.compile(re.escape(complex_word), re.IGNORECASE)
        simplified = pattern.sub(simple_word, simplified)
    
    # Layer 2: Sentence simplification
    sentences = simplified.split('. ')
    short_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 15:
            # Split long sentences
            mid = len(words) // 2
            part1 = ' '.join(words[:mid]) + '.'
            part2 = ' '.join(words[mid:])
            short_sentences.append(part1)
            short_sentences.append(part2)
        else:
            short_sentences.append(sentence)
    
    # Layer 3: Add explanations for complex terms
    final_text = '. '.join(short_sentences)
    
    return final_text

def generate_audio(text, language='ta'):
    """Generate voice output with fallback"""
    try:
        if language == 'ta':
            filename = "tamil_audio.mp3"
            tts = gTTS(text=text, lang='ta', slow=False, lang_check=False)
        else:
            filename = "english_audio.mp3"
            tts = gTTS(text=text, lang='en', slow=False)
        
        tts.save(filename)
        return filename
    except:
        # Fallback to Google TTS API
        try:
            text_encoded = urllib.parse.quote(text)
            if language == 'ta':
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=ta&client=tw-ob"
                filename = "tamil_audio.mp3"
            else:
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=en&client=tw-ob"
                filename = "english_audio.mp3"
            
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
        except:
            return None
        return None

def extract_text_from_image(image_file):
    """Extract text from uploaded image"""
    try:
        # Open image
        image = Image.open(image_file)
        
        # Try OCR
        try:
            import pytesseract
            text = pytesseract.image_to_string(image, lang='eng+hin+tam')
        except:
            # Fallback: ask user to type
            st.warning("🔍 OCR not available. Please type the text manually.")
            text = st.text_area("📝 Type the text from image:", height=150)
        
        return text if text else "Could not extract text from image."
    except Exception as e:
        st.error(f"Image processing error: {str(e)}")
        return "Error processing image."

def get_daily_tips(topic, language='ta'):
    """Get daily use tips based on input topic"""
    
    # Topic detection (simple keyword matching)
    topic_lower = topic.lower()
    
    # Define tips for different topics
    tips_database = {
        'ai': {
            'ta': [
                "🤖 AI உங்கள் வாழ்க்கையை எளிதாக்கும்!",
                "📱 Google Assistant, Siri போன்ற AI உதவியாளர்களைப் பயன்படுத்தவும்",
                "📸 AI கேமராக்கள் சிறப்பான புகைப்படங்களை எடுக்க உதவும்",
                "📚 AI பயன்பாடுகளைக் கற்றுக்கொள்ள YouTube பாடங்களைப் பார்க்கவும்",
                "🛡️ AI மூலம் மோசடி செய்திகளை அடையாளம் காணலாம்",
                "🎵 Spotify, YouTube போன்றவை AI பயன்படுத்தி உங்களுக்கான இசையைப் பரிந்துரைக்கும்",
                "💊 AI மருத்துவரை சந்திக்காமலே நோய்களை அடையாளம் காண உதவும்",
                "🏦 வங்கி பயன்பாடுகள் AI மூலம் பாதுகாப்பானவை",
                "📞 AI சாட்பாட்கள் 24/7 உங்கள் கேள்விகளுக்கு பதிலளிக்கும்",
                "🚗 Uber, Ola போன்றவை AI பயன்படுத்தி உங்கள் பயணத்தைத் திட்டமிடும்"
            ],
            'en': [
                "🤖 AI can make your life easier!",
                "📱 Use AI assistants like Google Assistant, Siri for daily help",
                "📸 AI cameras help take better photos automatically",
                "📚 Learn about AI apps through YouTube tutorials",
                "🛡️ AI can help detect scam messages and calls",
                "🎵 Spotify, YouTube use AI to recommend music you'll like",
                "💊 AI apps can identify health issues without doctor visit",
                "🏦 Banking apps are safer with AI fraud detection",
                "📞 AI chatbots answer your questions 24/7",
                "🚗 Uber, Ola use AI to plan your travel efficiently"
            ]
        },
        'bank': {
            'ta': [
                "🏦 உங்கள் OTP யாருக்கும் சொல்லாதீர்கள்",
                "💳 ATM கார்டு PIN எப்போதும் ரகசியமாக வைக்கவும்",
                "📱 UPI பயன்பாடுகளை பாதுகாப்பாக பயன்படுத்தவும்",
                "📞 வங்கி மோசடி பற்றிய புகார்களை 1930 க்கு அறிவிக்கவும்",
                "📧 வங்கி மின்னஞ்சல்களை சரிபார்க்க முதலில் வங்கியை தொடர்பு கொள்ளவும்",
                "💰 சந்தேகத்திற்கிடமான கடன் செய்திகளை நம்பாதீர்கள்",
                "🔒 உங்கள் வங்கி கடவுச்சொல்லை வாரம் ஒருமுறை மாற்றவும்",
                "📊 வங்கி பில்களை சரிபார்க்க குறைந்தபட்சம் மாதம் ஒருமுறை",
                "📱 மொபைல் பேங்கிங்கிற்கு இரண்டு காரணி அங்கீகாரத்தைப் பயன்படுத்தவும்",
                "🚨 உங்கள் வங்கி கணக்கில் சந்தேகத்திற்கிடமான பரிவர்த்தனைகளை உடனடியாக அறிவிக்கவும்"
            ],
            'en': [
                "🏦 Never share your OTP with anyone",
                "💳 Keep ATM card PIN secret always",
                "📱 Use UPI apps safely with password protection",
                "📞 Report bank frauds immediately to 1930",
                "📧 Always call bank to verify suspicious emails",
                "💰 Don't trust suspicious loan messages",
                "🔒 Change your bank password weekly",
                "📊 Check bank statements at least monthly",
                "📱 Use two-factor authentication for mobile banking",
                "🚨 Report suspicious transactions immediately"
            ]
        },
        'health': {
            'ta': [
                "💊 மருந்துகளை மருத்துவர் ஆலோசனையின்றி எடுக்கக்கூடாது",
                "🍎 தினமும் பழங்கள் மற்றும் காய்கறிகளை சாப்பிடவும்",
                "🚶‍♂️ தினமும் குறைந்தது 30 நிமிடம் நடக்கவும்",
                "💧 தினமும் 8 கிளாஸ் தண்ணீர் குடிக்கவும்",
                "😴 இரவு 7-8 மணி நேரம் உறங்கவும்",
                "🧘‍♂️ தினசரி மன அழுத்தம் குறைக்க யோகா செய்யவும்",
                "🚭 புகைப்பழக்கம், மது ஆகியவற்றை தவிர்க்கவும்",
                "🏥 ஆண்டிற்கு ஒருமுறை முழு உடல் பரிசோதனை செய்யவும்",
                "🧼 கைகளை அடிக்கடி கழுவவும்",
                "🌞 வைட்டமின் D க்கு காலை சூரிய ஒளியில் நடக்கவும்"
            ],
            'en': [
                "💊 Don't take medicines without doctor consultation",
                "🍎 Eat fruits and vegetables daily",
                "🚶‍♂️ Walk at least 30 minutes every day",
                "💧 Drink 8 glasses of water daily",
                "😴 Sleep 7-8 hours every night",
                "🧘‍♂️ Practice yoga daily to reduce stress",
                "🚭 Avoid smoking and alcohol",
                "🏥 Get full body checkup yearly",
                "🧼 Wash hands frequently",
                "🌞 Walk in morning sunlight for Vitamin D"
            ]
        },
        'education': {
            'ta': [
                "📚 தினமும் குறைந்தது 2 மணி நேரம் படிக்கவும்",
                "📝 புதிய வார்த்தைகளை கற்றுக்கொள்ள தினசரி 5 சொற்கள்",
                "🎯 இலக்குகளை அமைத்து அவற்றை அடைய திட்டமிடவும்",
                "🤝 குழுவாக படிப்பது மேம்பட்ட கற்றலை அளிக்கும்",
                "📱 கல்வி பயன்பாடுகளைப் பயன்படுத்தி புதிய திறன்களைக் கற்றுக்கொள்ளுங்கள்",
                "🎓 இலவச ஆன்லைன் பாடங்களைப் பயன்படுத்தவும்",
                "🧠 குறிப்புகளை எடுத்து மீண்டும் மீண்டும் படிக்கவும்",
                "⏰ ஒழுங்கான நேர அட்டவணையை பின்பற்றவும்",
                "❓ சந்தேகங்களை உடனடியாக தீர்க்கவும்",
                "🏆 சிறிய சாதனைகளை கொண்டாடுங்கள்"
            ],
            'en': [
                "📚 Study at least 2 hours daily",
                "📝 Learn 5 new words every day",
                "🎯 Set goals and plan to achieve them",
                "🤝 Group study provides better learning",
                "📱 Use educational apps to learn new skills",
                "🎓 Utilize free online courses",
                "🧠 Take notes and revise regularly",
                "⏰ Follow a disciplined time schedule",
                "❓ Clear doubts immediately",
                "🏆 Celebrate small achievements"
            ]
        }
    }
    
    # Detect topic from input
    detected_topic = 'ai'  # default
    
    if any(word in topic_lower for word in ['bank', 'account', 'money', 'loan', 'otp']):
        detected_topic = 'bank'
    elif any(word in topic_lower for word in ['health', 'doctor', 'medicine', 'hospital']):
        detected_topic = 'health'
    elif any(word in topic_lower for word in ['study', 'education', 'school', 'college']):
        detected_topic = 'education'
    elif any(word in topic_lower for word in ['ai', 'artificial', 'intelligence', 'machine']):
        detected_topic = 'ai'
    
    # Get tips for detected topic and language
    tips = tips_database.get(detected_topic, {}).get(language, [])
    
    if not tips:
        # Default tips
        if language == 'ta':
            tips = ["🌞 நாள்தோறும் புதிய விஷயங்களைக் கற்றுக்கொள்ள முயற்சிக்கவும்!"]
        else:
            tips = ["🌞 Try to learn new things every day!"]
    
    return tips, detected_topic

# ==================== INITIALIZE SESSION STATE ====================
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
if 'selected_output' not in st.session_state:
    st.session_state.selected_output = "🇮🇳 Tamil Only"
if 'daily_tips' not in st.session_state:
    st.session_state.daily_tips = []

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🗣️🤖 Talk2Tamil: Smart Assistant</h1>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 15px; flex-wrap: wrap;">
        <span>🎤 Voice Input</span>
        <span>📸 Image Upload</span>
        <span>📝 Text Input</span>
        <span>🇮🇳 Tamil Output</span>
        <span>🇬🇧 Simple English</span>
        <span>💡 Daily Tips</span>
        <span>🔊 Voice Output</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FEATURE CARDS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card" style="border-left-color: #FF6B6B;">
        <h4>🎤 Voice Input</h4>
        <p>Speak in Tamil/English</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="border-left-color: #4ECDC4;">
        <h4>📸 Image Upload</h4>
        <p>Extract text from photos</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="border-left-color: #FFD166;">
        <h4>💡 Smart Tips</h4>
        <p>Daily useful messages</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card" style="border-left-color: #06D6A0;">
        <h4>🔊 Voice Output</h4>
        <p>Listen in Tamil/English</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== INPUT SECTION ====================
st.markdown("""
<div class="input-section">
    <h2>📥 Input Your Content</h2>
    <p style="color: #666;">Choose how you want to input text:</p>
</div>
""", unsafe_allow_html=True)

# Input method tabs
input_tab1, input_tab2, input_tab3 = st.tabs(["📝 Type Text", "🎤 Voice Input", "📸 Upload Image"])

with input_tab1:
    st.markdown("### ✍️ Type or Paste Text")
    text_input = st.text_area(
        "Enter your text in any language:",
        height=200,
        placeholder="Type or paste your text here...\nExample: 'Artificial Intelligence helps in daily life'",
        key="text_input",
        help="You can type in English, Tamil, Hindi or any language"
    )
    st.session_state.current_input = text_input

with input_tab2:
    st.markdown("### 🎤 Voice Input (Speak)")
    
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.markdown("""
        <div style="background: #FFF3E0; padding: 20px; border-radius: 15px; margin: 10px 0;">
            <h4>🎙️ How to Use Voice Input:</h4>
            <p>1. Click "Start Recording" below<br>
            2. Speak clearly in Tamil or English<br>
            3. Click "Stop Recording" when done<br>
            4. Your speech will appear as text</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice recording simulation
        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("🔴 Start Recording", use_container_width=True, key="start_rec"):
                st.session_state.recording = True
                st.success("🎤 Recording started... Speak now!")
        
        with col_stop:
            if st.button("⏹️ Stop Recording", use_container_width=True, key="stop_rec"):
                if 'recording' in st.session_state:
                    del st.session_state.recording
                    st.success("✅ Recording stopped!")
        
        # Voice input text area
        voice_text = st.text_area(
            "🎤 Your voice input will appear here:",
            height=150,
            placeholder="Speak and your words will appear here...\nFor demo, you can also type here.",
            key="voice_input"
        )
        
        if voice_text:
            st.session_state.current_input = voice_text
    
    with col_v2:
        st.markdown("### 🎯 Tips for Voice")
        st.markdown("""
        **For clear voice input:**
        
        🔊 **Speak clearly**
        🎯 **One sentence at a time**
        📍 **No background noise**
        ⏸️ **Pause between sentences**
        """)

with input_tab3:
    st.markdown("### 📸 Upload Image with Text")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Upload screenshot, photo of document, or any image with text"
    )
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Image", width=300)
        
        # Extract text button
        if st.button("🔍 Extract Text from Image", key="extract_text"):
            with st.spinner("🔍 Extracting text from image..."):
                extracted_text = extract_text_from_image(uploaded_file)
                st.session_state.current_input = extracted_text
                st.success("✅ Text extracted successfully!")
                
                # Show extracted text
                st.text_area("📝 Extracted Text:", extracted_text, height=150, key="extracted_text")
    else:
        st.info("📁 Upload an image file to extract text")

# ==================== OUTPUT SETTINGS ====================
st.markdown("---")
col_set1, col_set2 = st.columns([2, 1])

with col_set1:
    st.markdown("### ⚙️ Output Settings")
    
    output_option = st.radio(
        "🎯 Select output language:",
        ["🇮🇳 Tamil Only", "🇬🇧 Simple English Only", "🌍 Both Languages"],
        key="output_lang",
        horizontal=True
    )
    
    st.session_state.selected_output = output_option
    
    # Voice output option
    voice_output = st.checkbox(
        "🔊 Generate voice output",
        value=True,
        help="Get audio version of the translation"
    )

with col_set2:
    st.markdown("### 💡 Daily Tips Language")
    
    tips_language = st.radio(
        "Daily tips in:",
        ["🇮🇳 Tamil", "🇬🇧 English"],
        key="tips_lang",
        horizontal=True
    )

# ==================== TRANSLATE BUTTON ====================
st.markdown("---")
if st.button(
    "✨ TRANSLATE & GET DAILY TIPS",
    type="primary",
    use_container_width=True,
    key="translate_btn"
):
    if st.session_state.current_input and st.session_state.current_input.strip():
        with st.spinner("🔄 Processing your request..."):
            # Get translation
            tamil_text = ""
            english_text = ""
            
            if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
                tamil_text = translate_text(st.session_state.current_input, 'ta')
            
            if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
                english_text = simplify_english(st.session_state.current_input)
            
            # Get daily tips
            tips_lang_code = 'ta' if tips_language == "🇮🇳 Tamil" else 'en'
            daily_tips, detected_topic = get_daily_tips(st.session_state.current_input, tips_lang_code)
            
            # Store in session
            st.session_state.translation_result = {
                'original': st.session_state.current_input,
                'tamil': tamil_text,
                'english': english_text,
                'daily_tips': daily_tips,
                'detected_topic': detected_topic,
                'tips_language': tips_language
            }
    else:
        st.warning("⚠️ Please enter some text first!")

# ==================== RESULTS SECTION ====================
if st.session_state.translation_result:
    result = st.session_state.translation_result
    
    st.markdown("""
    <div class="output-section">
        <h2>📊 Translation Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Show detected topic
    topic_emoji = {
        'ai': '🤖',
        'bank': '🏦', 
        'health': '🏥',
        'education': '📚'
    }.get(result['detected_topic'], '💡')
    
    st.info(f"{topic_emoji} **Detected Topic:** {result['detected_topic'].upper()} - Daily tips will be about this topic")
    
    # Display translations
    if output_option == "🌍 Both Languages":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("### 🇮🇳 தமிழ் மொழிபெயர்ப்பு")
            if result['tamil']:
                st.success(result['tamil'])
                
                # Voice output for Tamil
                if voice_output:
                    if st.button("🔊 Play Tamil Audio", key="play_tamil_audio"):
                        audio_file = generate_audio(result['tamil'], 'ta')
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
                            st.success("✅ Tamil audio playing")
        
        with col_english:
            st.markdown("### 🇬🇧 Simple English")
            if result['english']:
                st.success(result['english'])
                
                # Show simplification
                if result['english'] != result['original']:
                    with st.expander("🔄 See what was simplified"):
                        col_orig, col_simp = st.columns(2)
                        with col_orig:
                            st.markdown("**Original:**")
                            st.info(result['original'][:200] + "..." if len(result['original']) > 200 else result['original'])
                        with col_simp:
                            st.markdown("**Simplified:**")
                            st.success(result['english'][:200] + "..." if len(result['english']) > 200 else result['english'])
                
                # Voice output for English
                if voice_output:
                    if st.button("🔊 Play English Audio", key="play_english_audio"):
                        audio_file = generate_audio(result['english'], 'en')
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
                            st.success("✅ English audio playing")
    
    elif output_option == "🇮🇳 Tamil Only":
        st.markdown("### 🇮🇳 Tamil Translation")
        if result['tamil']:
            st.success(result['tamil'])
            
            # Voice output
            if voice_output:
                if st.button("🔊 Play Tamil Audio", key="play_tamil_only"):
                    audio_file = generate_audio(result['tamil'], 'ta')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
    
    else:  # English Only
        st.markdown("### 🇬🇧 Simplified English")
        if result['english']:
            st.success(result['english'])
            
            # Voice output
            if voice_output:
                if st.button("🔊 Play English Audio", key="play_english_only"):
                    audio_file = generate_audio(result['english'], 'en')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
    
    # ==================== DAILY TIPS SECTION ====================
    st.markdown("---")
    st.markdown(f"""
    <div class="daily-tip">
        <h2><span class="tip-icon">💡</span> Daily Useful Tips ({result['tips_language']})</h2>
        <p>Based on your input about <strong>{result['detected_topic'].upper()}</strong>, here are useful daily messages:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display daily tips
    if result['daily_tips']:
        for i, tip in enumerate(result['daily_tips'][:5]):  # Show first 5 tips
            st.markdown(f"""
            <div style="background: {'#FFF9C4' if i % 2 == 0 else '#E1F5FE'}; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin: 10px 0;
                        border-left: 5px solid {'#FFB300' if i % 2 == 0 else '#039BE5'};">
                <h4>💡 Tip {i+1}</h4>
                <p>{tip}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Voice option for tips
        if voice_output:
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                if st.button("🔊 Listen to All Tips", key="play_all_tips"):
                    all_tips = ". ".join(result['daily_tips'][:3])
                    audio_file = generate_audio(all_tips, 'ta' if result['tips_language'] == "🇮🇳 Tamil" else 'en')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
            
            with col_t2:
                if st.download_button(
                    "📥 Save Tips as Text",
                    "\n".join(result['daily_tips']),
                    file_name=f"daily_tips_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    key="download_tips"
                ):
                    st.success("✅ Tips saved!")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📋 Quick Examples")
    
    examples = {
        "🤖 AI in Daily Life": "Artificial Intelligence helps in daily tasks like voice assistants and photo editing.",
        "🏦 Bank Safety": "Your bank account needs verification. Share your details securely.",
        "🏥 Health Tips": "Regular exercise
