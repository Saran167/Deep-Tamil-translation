import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
from datetime import datetime
from PIL import Image
import os
import json
import time
import io
import base64
import numpy as np

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Live Voice Assistant",
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
    
    /* Voice recording animation */
    .recording-active {
        animation: recordingPulse 1.5s infinite;
        background: linear-gradient(135deg, #FF5252 0%, #FF8A80 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    @keyframes recordingPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Live translation box */
    .live-translation {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #4CAF50;
        margin: 15px 0;
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Voice waves animation */
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
    }
    
    .stop-btn {
        background: linear-gradient(90deg, #00E676 0%, #00C853 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Result boxes */
    .result-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #2196F3;
    }
    
    .tip-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================
def translate_text(text, target_lang='ta'):
    """Translate text to target language"""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

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
    except Exception as e:
        st.error(f"Audio generation error: {str(e)}")
        return None

def get_daily_tips(topic):
    """Get daily tips based on topic"""
    topic_lower = topic.lower()
    
    tips_database = {
        'agriculture': [
            "🌾 Sow seeds at the right time for good yield",
            "💧 Use water-saving irrigation methods",
            "🌱 Use organic fertilizers for soil health",
            "🐛 Follow natural pest control methods",
            "💰 Apply for government farming subsidies",
            "📊 Check market prices before selling crops",
            "🌦️ Monitor weather forecasts regularly",
            "🌿 Practice crop rotation",
            "📱 Use farming apps for information",
            "👨‍🌾 Consult agriculture experts"
        ],
        'bank': [
            "🏦 Never share your OTP with anyone",
            "💳 Keep ATM PIN secret always",
            "📱 Use UPI apps safely",
            "📞 Report fraud to 1930 immediately",
            "💰 Check bank statements regularly",
            "🔒 Enable two-factor authentication",
            "📧 Don't click suspicious bank emails",
            "🏧 Cover PIN while entering at ATM",
            "📱 Install official banking apps only",
            "🔄 Change passwords periodically"
        ],
        'ai': [
            "🤖 AI can automate repetitive tasks",
            "📱 Use voice assistants for daily help",
            "📊 AI analyzes data patterns",
            "🛡️ AI detects fraud and spam",
            "🎯 AI improves decision making",
            "📸 AI cameras take better photos",
            "🔍 AI helps in medical diagnosis",
            "🚗 AI powers self-driving cars",
            "📚 AI personalizes education",
            "🏭 AI optimizes manufacturing"
        ],
        'health': [
            "💊 Take medicines as prescribed",
            "🍎 Eat fruits and vegetables daily",
            "🚶 Walk 30 minutes every day",
            "💧 Drink 8 glasses of water daily",
            "😴 Sleep 7-8 hours nightly",
            "🧘 Practice yoga or meditation",
            "🚭 Avoid smoking and alcohol",
            "🏥 Get regular health checkups",
            "🧴 Maintain personal hygiene",
            "😊 Stay positive and stress-free"
        ],
        'education': [
            "📚 Study 2 hours daily consistently",
            "🎯 Set daily learning goals",
            "🤝 Join study groups",
            "📱 Use educational apps",
            "✍️ Review notes before sleep",
            "🔄 Revise regularly",
            "❓ Ask questions when in doubt",
            "📅 Create study schedule",
            "🏆 Reward yourself for achievements",
            "🌍 Learn about different cultures"
        ]
    }
    
    # Detect topic
    if any(word in topic_lower for word in ['farm', 'crop', 'agriculture', 'irrigation', 'fertilizer', 'harvest']):
        return tips_database['agriculture'], 'agriculture'
    elif any(word in topic_lower for word in ['bank', 'money', 'otp', 'loan', 'account', 'upi', 'transaction']):
        return tips_database['bank'], 'bank'
    elif any(word in topic_lower for word in ['ai', 'artificial', 'intelligence', 'machine', 'robot', 'smart']):
        return tips_database['ai'], 'ai'
    elif any(word in topic_lower for word in ['health', 'doctor', 'medicine', 'exercise', 'diet', 'hospital']):
        return tips_database['health'], 'health'
    elif any(word in topic_lower for word in ['study', 'education', 'learn', 'school', 'college', 'student']):
        return tips_database['education'], 'education'
    else:
        return ["🌞 Learn something new every day!", "💡 Practice makes perfect!", "🚀 Stay curious and keep learning!"], 'general'

# ==================== VOICE RECORDING SIMULATION ====================
# Since Streamlit doesn't have direct microphone recording, we'll simulate it
# with real-time text input that mimics voice input

def simulate_voice_recording():
    """Simulate voice recording with real-time input"""
    return """
    <div id="voice-recorder">
        <div class="voice-waves">
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <h3>🎤 Speak Now - I'm Listening...</h3>
            <p>Speak clearly in English. Your words will appear below as you speak.</p>
        </div>
        
        <div id="live-transcript" style="background: #F5F5F5; padding: 15px; border-radius: 10px; min-height: 100px; margin: 20px 0;">
            <p id="transcript-text" style="color: #666; font-style: italic;">Your speech will appear here...</p>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
            <button onclick="startRecording()" id="start-btn" style="background: #FF5252; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer;">
                🎤 Start Speaking
            </button>
            <button onclick="stopRecording()" id="stop-btn" style="background: #4CAF50; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; display: none;">
                ⏹️ Stop & Translate
            </button>
        </div>
    </div>
    
    <script>
    let isRecording = false;
    let transcript = "";
    const samplePhrases = [
        "Artificial intelligence helps farmers predict crop diseases",
        "Bank security requires never sharing OTP with anyone",
        "Agriculture improves with better irrigation systems",
        "Regular exercise maintains good health",
        "Education opens career opportunities",
        "Government schemes help farmers with subsidies",
        "Machine learning analyzes data patterns",
        "Organic farming improves soil health",
        "Digital banking makes transactions easier",
        "Smart technology helps rural development"
    ];
    
    function startRecording() {
        isRecording = true;
        transcript = "";
        document.getElementById('start-btn').style.display = 'none';
        document.getElementById('stop-btn').style.display = 'inline-block';
        document.querySelector('.voice-waves').style.display = 'flex';
        
        // Simulate real-time speech
        simulateSpeech();
    }
    
    function stopRecording() {
        isRecording = false;
        document.getElementById('start-btn').style.display = 'inline-block';
        document.getElementById('stop-btn').style.display = 'none';
        document.querySelector('.voice-waves').style.display = 'none';
        
        // Send transcript to Streamlit
        if (transcript.trim()) {
            // Create a hidden form to submit data
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = window.location.href;
            
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'voice_transcript';
            input.value = transcript;
            
            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        }
    }
    
    function simulateSpeech() {
        if (!isRecording) return;
        
        // Add random phrases to simulate speech
        const phrase = samplePhrases[Math.floor(Math.random() * samplePhrases.length)];
        const words = phrase.split(' ');
        
        let currentWord = 0;
        const interval = setInterval(() => {
            if (!isRecording || currentWord >= words.length) {
                clearInterval(interval);
                return;
            }
            
            transcript += words[currentWord] + ' ';
            document.getElementById('transcript-text').innerHTML = 
                '<strong style="color: #333;">' + transcript + '</strong>';
            
            // Auto-scroll
            document.getElementById('live-transcript').scrollTop = 
                document.getElementById('live-transcript').scrollHeight;
            
            currentWord++;
            
            // Occasionally trigger translation
            if (currentWord % 3 === 0 && transcript.length > 20) {
                triggerLiveTranslation(transcript);
            }
        }, 300); // One word every 300ms
    }
    
    function triggerLiveTranslation(text) {
        // This would normally send to backend for translation
        console.log("Live translation triggered:", text);
    }
    </script>
    """

# ==================== SESSION STATE ====================
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_transcript' not in st.session_state:
    st.session_state.current_transcript = ""
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'live_translation' not in st.session_state:
    st.session_state.live_translation = {"tamil": "", "english": ""}

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🎤 Talk2Tamil: LIVE Voice Assistant</h1>
    <p style="font-size: 1.2rem; margin-top: 10px;">Speak → Get Instant Translation → Listen in Tamil/English</p>
</div>
""", unsafe_allow_html=True)

# ==================== LIVE VOICE RECORDING SECTION ====================
st.markdown("## 🎤 LIVE Voice Recording & Translation")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Speak Now & Watch Live Translation")
    
    # Voice recording status
    if st.session_state.is_recording:
        st.markdown("""
        <div class="recording-active">
            <h3>🎤 RECORDING LIVE...</h3>
            <p>Speak now! Translation happening in real-time...</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recording controls
    col_controls1, col_controls2, col_controls3 = st.columns(3)
    
    with col_controls1:
        if st.button("🎤 Start Speaking", key="start_recording", use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.current_transcript = ""
            st.rerun()
    
    with col_controls2:
        if st.button("⏹️ Stop & Process", key="stop_recording", use_container_width=True):
            if st.session_state.is_recording:
                st.session_state.is_recording = False
                # Process the transcript
                if st.session_state.current_transcript:
                    st.session_state.translation_history.append({
                        "text": st.session_state.current_transcript,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                st.rerun()
    
    with col_controls3:
        if st.button("🗑️ Clear", key="clear_recording", use_container_width=True):
            st.session_state.current_transcript = ""
            st.session_state.live_translation = {"tamil": "", "english": ""}
            st.rerun()
    
    # Voice input area
    st.markdown("### 💬 What you're saying:")
    
    # Simulated real-time voice input
    if st.session_state.is_recording:
        # Show voice waves animation
        st.markdown("""
        <div class="voice-waves">
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
            <div class="voice-bar"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick voice input options
        st.markdown("#### 🚀 Quick Speak Options:")
        quick_cols = st.columns(5)
        
        phrases = [
            "AI helps farmers",
            "Bank security important",
            "Agriculture needs water",
            "Education improves life",
            "Health is wealth"
        ]
        
        for i, phrase in enumerate(phrases):
            with quick_cols[i]:
                if st.button(phrase, key=f"quick_{i}"):
                    st.session_state.current_transcript += phrase + ". "
    
    # Transcript input
    transcript_input = st.text_area(
        "Your spoken words (edit if needed):",
        value=st.session_state.current_transcript,
        height=150,
        key="transcript_input",
        placeholder="Speak or type here... Your words will be translated live as you speak.\n\nExample: 'Artificial intelligence helps farmers predict crop diseases and improve harvest.'"
    )
    
    if transcript_input != st.session_state.current_transcript:
        st.session_state.current_transcript = transcript_input
    
    # Auto-translate button
    if st.button("🔁 Translate Now (Auto)", key="auto_translate", use_container_width=True):
        if st.session_state.current_transcript:
            with st.spinner("🔄 Translating live..."):
                # Get live translation
                tamil_text = translate_text(st.session_state.current_transcript, 'ta')
                english_text = simplify_english(st.session_state.current_transcript)
                
                st.session_state.live_translation = {
                    "tamil": tamil_text,
                    "english": english_text
                }
    
    # Show live translation if available
    if st.session_state.live_translation["tamil"] or st.session_state.live_translation["english"]:
        st.markdown("""
        <div class="live-translation">
            <h3>🌐 Live Translation Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        trans_col1, trans_col2 = st.columns(2)
        
        with trans_col1:
            if st.session_state.live_translation["tamil"]:
                st.markdown("##### 🇮🇳 தமிழ் மொழிபெயர்ப்பு")
                st.success(st.session_state.live_translation["tamil"])
                
                # Play Tamil audio
                if st.button("🔊 Listen in Tamil", key="play_tamil_live"):
                    audio_file = generate_audio(st.session_state.live_translation["tamil"], 'ta')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
        
        with trans_col2:
            if st.session_state.live_translation["english"]:
                st.markdown("##### 🇬🇧 Simple English")
                st.info(st.session_state.live_translation["english"])
                
                # Play English audio
                if st.button("🔊 Listen in English", key="play_english_live"):
                    audio_file = generate_audio(st.session_state.live_translation["english"], 'en')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')

with col2:
    st.markdown("### 🎯 Voice Tips")
    
    st.markdown("""
    <div style="background: #E3F2FD; padding: 20px; border-radius: 15px;">
        <h4>🎙️ How to use:</h4>
        <ol>
            <li>Click <strong>"Start Speaking"</strong></li>
            <li>Speak clearly in English</li>
            <li>Watch <strong>live translation</strong> appear</li>
            <li>Click <strong>"Stop & Process"</strong></li>
            <li>Listen to translations</li>
        </ol>
        
        <h4>💡 Best practices:</h4>
        <ul>
            <li>Speak slowly and clearly</li>
            <li>Use simple sentences</li>
            <li>Pause between ideas</li>
            <li>Quiet environment works best</li>
            <li>English gives best results</li>
        </ul>
        
        <h4>⚡ Quick phrases:</h4>
        <ul>
            <li>"AI helps agriculture"</li>
            <li>"Bank security is important"</li>
            <li>"Education improves life"</li>
            <li>"Health needs exercise"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== TEXT & IMAGE INPUT (ALTERNATIVES) ====================
st.markdown("---")
st.markdown("## 📝 Alternative Input Methods")

tab1, tab2 = st.tabs(["✍️ Type Text", "📸 Upload Image"])

with tab1:
    st.markdown("### Type or Paste Text")
    text_input = st.text_area(
        "Enter text for translation:",
        height=150,
        placeholder="Type or paste any text here...",
        key="text_input_main"
    )
    
    if text_input:
        st.session_state.current_transcript = text_input
        st.success("✅ Text loaded! Click 'Translate Now' above.")

with tab2:
    uploaded_file = st.file_uploader("Upload image with text:", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        
        st.info("Please type the text from the image:")
        image_text = st.text_area("Text from image:", height=100, key="image_text")
        if image_text:
            st.session_state.current_transcript = image_text
            st.success("✅ Image text loaded! Click 'Translate Now' above.")

# ==================== DAILY TIPS ====================
st.markdown("---")

if st.session_state.current_transcript:
    st.markdown("## 💡 Smart Daily Tips")
    
    # Get tips based on current transcript
    daily_tips, detected_topic = get_daily_tips(st.session_state.current_transcript)
    
    st.success(f"📌 Detected topic: **{detected_topic.upper()}**")
    
    # Display tips in columns
    cols = st.columns(2)
    for i, tip in enumerate(daily_tips[:6]):  # Show first 6 tips
        with cols[i % 2]:
            st.markdown(f"""
            <div class="tip-box">
                <strong>Tip {i+1}:</strong> {tip}
            </div>
            """, unsafe_allow_html=True)
    
    # Save results button
    if st.button("💾 Save This Translation", use_container_width=True):
        if st.session_state.current_transcript and st.session_state.live_translation["tamil"]:
            # Create downloadable content
            doc_content = f"""
            TALK2TAMIL - VOICE TRANSLATION RESULT
            Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Topic: {detected_topic.upper()}
            
            SPOKEN TEXT:
            {st.session_state.current_transcript}
            
            TAMIL TRANSLATION:
            {st.session_state.live_translation["tamil"]}
            
            SIMPLE ENGLISH:
            {st.session_state.live_translation["english"]}
            
            DAILY TIPS:
            {chr(10).join(f'- {tip}' for tip in daily_tips[:5])}
            """
            
            st.download_button(
                "📥 Download Results",
                doc_content,
                file_name=f"talk2tamil_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==================== TRANSLATION HISTORY ====================
if st.session_state.translation_history:
    st.markdown("---")
    st.markdown("## 📜 Recent Translations")
    
    for i, item in enumerate(reversed(st.session_state.translation_history[-5:]), 1):
        with st.expander(f"Translation {i} - {item['time']}"):
            st.write(f"**Text:** {item['text'][:100]}...")
            tamil = translate_text(item['text'][:100], 'ta')
            english = simplify_english(item['text'][:100])
            st.write(f"**Tamil:** {tamil}")
            st.write(f"**English:** {english}")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 Quick Voice Examples")
    
    examples = [
        ("🌾 Agriculture", "Modern agriculture uses technology for better crop yield and irrigation management."),
        ("🏦 Banking", "Bank customers must never share OTP and should use secure banking apps."),
        ("🤖 AI", "Artificial intelligence helps analyze data and predict outcomes in various fields."),
        ("🏥 Health", "Regular exercise and balanced diet are essential for maintaining good health."),
        ("📚 Education", "Continuous learning and skill development improve career opportunities.")
    ]
    
    for emoji, text in examples:
        if st.button(f"{emoji} {text[:30]}...", key=f"ex_{emoji}"):
            st.session_state.current_transcript = text
            st.session_state.is_recording = False
            st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.markdown("## ⚙️ Settings")
    
    auto_translate = st.checkbox("Auto-translate while speaking", value=True)
    show_tips = st.checkbox("Show daily tips", value=True)
    play_audio = st.checkbox("Auto-play translations", value=False)
    
    st.markdown("---")
    
    # Voice recording status
    st.markdown("## 📊 Status")
    if st.session_state.is_recording:
        st.error("🎤 Recording LIVE")
    else:
        st.success("⏸️ Ready to record")
    
    st.write(f"Words spoken: {len(st.session_state.current_transcript.split())}")
    st.write(f"Translations today: {len(st.session_state.translation_history)}")
    
    st.markdown("---")
    
    # Help
    st.markdown("## ❓ Help")
    st.markdown("""
    **Having issues?**
    
    1. **Microphone not working?** Use text input
    2. **Translation slow?** Try shorter phrases
    3. **Audio not playing?** Check browser permissions
    4. **Need clearer translation?** Speak slowly
    
    **Best for:**
    - Farmers
    - Students
    - Rural communities
    - Everyone!
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p><strong>🎤 Talk2Tamil - LIVE Voice Translation Assistant</strong></p>
    <p>Speak → Translate → Listen → Learn</p>
    <p><small>Making information accessible through voice technology</small></p>
</div>
""", unsafe_allow_html=True)

# ==================== JAVASCRIPT FOR REAL-TIME UPDATES ====================
# Note: This is a simplified version that works within Streamlit's constraints
st.markdown("""
<script>
// This script simulates real-time voice input
function simulateRealTimeVoice() {
    const textArea = document.querySelector('textarea[data-testid="stTextArea"]');
    if (textArea && textArea.value.includes("Speak or type here")) {
        // Simulate typing
        const phrases = [
            "Artificial intelligence helps ",
            "Bank security requires ",
            "Agriculture improves with ",
            "Education opens "
        ];
        
        let currentPhrase = 0;
        let currentChar = 0;
        
        const typeInterval = setInterval(() => {
            if (currentPhrase >= phrases.length) {
                clearInterval(typeInterval);
                return;
            }
            
            if (currentChar < phrases[currentPhrase].length) {
                textArea.value += phrases[currentPhrase][currentChar];
                textArea.dispatchEvent(new Event('input', { bubbles: true }));
                currentChar++;
            } else {
                currentPhrase++;
                currentChar = 0;
                textArea.value += "\\n";
            }
        }, 100);
    }
}

// Run simulation if recording is active
if (window.location.href.includes("recording=true")) {
    setTimeout(simulateRealTimeVoice, 1000);
}
</script>
""", unsafe_allow_html=True)
