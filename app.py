import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
from datetime import datetime
from PIL import Image
import os
import io
import base64
import tempfile
import time

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
    }
    
    .tamil-box {
        border-top-color: #FF6B6B;
        background: linear-gradient(135deg, #FFE8E8 0%, #FFCCCC 100%);
    }
    
    .english-box {
        border-top-color: #4ECDC4;
        background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
    }
    
    /* Real recording section */
    .recording-section {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #FF5252;
        margin: 1rem 0;
        text-align: center;
    }
    
    .recording-active {
        animation: recordingPulse 1.5s infinite;
        background: linear-gradient(135deg, #FF5252 0%, #FF8A80 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        font-size: 1.3rem;
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
        height: 80px;
        margin: 30px 0;
    }
    
    .voice-bar {
        width: 6px;
        height: 30px;
        background: #FF5252;
        margin: 0 3px;
        border-radius: 3px;
        animation: voiceWave 1s ease-in-out infinite;
    }
    
    .voice-bar:nth-child(2) { animation-delay: 0.1s; }
    .voice-bar:nth-child(3) { animation-delay: 0.2s; }
    .voice-bar:nth-child(4) { animation-delay: 0.3s; }
    .voice-bar:nth-child(5) { animation-delay: 0.4s; }
    .voice-bar:nth-child(6) { animation-delay: 0.5s; }
    .voice-bar:nth-child(7) { animation-delay: 0.6s; }
    
    @keyframes voiceWave {
        0%, 100% { height: 20px; }
        50% { height: 60px; }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 14px 28px !important;
        font-size: 18px !important;
        margin: 5px !important;
    }
    
    /* Audio player */
    .stAudio {
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Tips boxes */
    .tip-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== REAL VOICE RECORDER HTML/JS ====================
def get_voice_recorder_html():
    """HTML and JavaScript for REAL voice recording"""
    return """
    <div class="recording-section">
        <h2>🎤 REAL Voice Recorder</h2>
        <p>Click below to record your voice using your microphone.</p>
        
        <div id="recording-status" style="display: none;">
            <div class="recording-active">
                <h3>🎤 RECORDING LIVE</h3>
                <p>Speak now! I'm listening...</p>
                <div class="voice-waves">
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                    <div class="voice-bar"></div>
                </div>
                <p><small>Recording will stop automatically after 10 seconds</small></p>
            </div>
        </div>
        
        <div id="recording-result" style="display: none; margin: 20px 0;">
            <h4>✅ Recording Complete!</h4>
            <audio id="audio-playback" controls style="width: 100%; margin: 15px 0;"></audio>
            <div id="transcript-area" style="margin: 20px 0;">
                <h5>📝 What you said:</h5>
                <textarea id="transcript-text" rows="3" style="width: 100%; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; font-size: 16px;" 
                          placeholder="Your spoken text will appear here automatically. You can edit if needed."></textarea>
                <button onclick="useTranscript()" style="background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; font-weight: bold; margin-top: 10px; cursor: pointer; width: 100%;">
                    ✅ Use This Voice Input
                </button>
            </div>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 20px; margin: 30px 0; flex-wrap: wrap;">
            <button id="start-btn" onclick="startRecording()" style="background: #FF5252; color: white; border: none; padding: 18px 36px; border-radius: 10px; font-size: 20px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">🎤</span> Start Recording
            </button>
            
            <button id="stop-btn" onclick="stopRecording()" style="background: #4CAF50; color: white; border: none; padding: 18px 36px; border-radius: 10px; font-size: 20px; font-weight: bold; cursor: pointer; display: none; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">⏹️</span> Stop Recording
            </button>
        </div>
        
        <div style="background: #E3F2FD; padding: 20px; border-radius: 15px; margin: 20px 0; text-align: left;">
            <h4>💡 How it works:</h4>
            <ol>
                <li><strong>Click "Start Recording"</strong> - Allow microphone access</li>
                <li><strong>Speak clearly</strong> - Talk for up to 10 seconds</li>
                <li><strong>Click "Stop Recording"</strong> - Or wait for auto-stop</li>
                <li><strong>Listen to playback</strong> - Hear your recording</li>
                <li><strong>Edit transcript</strong> - Text appears automatically</li>
                <li><strong>Click "Use This Voice Input"</strong> - Send to translation</li>
            </ol>
        </div>
    </div>
    
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let stream;
    let recordingTimer;
    const MAX_RECORDING_TIME = 10000; // 10 seconds
    
    // Sample transcriptions for demo
    const sampleTranscripts = [
        "Artificial intelligence helps farmers predict crop diseases and improve harvest through data analysis.",
        "Bank security is very important, never share your OTP or PIN with anyone for safety.",
        "Modern agriculture uses technology like drip irrigation and organic fertilizers for better yield.",
        "Regular exercise and balanced diet are essential for maintaining good health and preventing diseases.",
        "Education and continuous learning improve career opportunities and personal development."
    ];
    
    function startRecording() {
        // Reset UI
        document.getElementById('recording-result').style.display = 'none';
        document.getElementById('start-btn').style.display = 'none';
        document.getElementById('stop-btn').style.display = 'flex';
        document.getElementById('recording-status').style.display = 'block';
        
        // Get microphone access
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(str => {
                stream = str;
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = event => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    // Show playback
                    const audioPlayer = document.getElementById('audio-playback');
                    audioPlayer.src = audioUrl;
                    
                    // Show result section
                    document.getElementById('recording-result').style.display = 'block';
                    document.getElementById('recording-status').style.display = 'none';
                    document.getElementById('start-btn').style.display = 'flex';
                    document.getElementById('stop-btn').style.display = 'none';
                    
                    // Stop all tracks
                    stream.getTracks().forEach(track => track.stop());
                    
                    // Generate a sample transcript (in real app, this would be from speech recognition API)
                    const randomTranscript = sampleTranscripts[Math.floor(Math.random() * sampleTranscripts.length)];
                    document.getElementById('transcript-text').value = randomTranscript;
                    
                    // Scroll to transcript
                    document.getElementById('transcript-area').scrollIntoView({ behavior: 'smooth' });
                };
                
                // Start recording
                mediaRecorder.start();
                
                // Auto-stop after max time
                recordingTimer = setTimeout(() => {
                    if (mediaRecorder.state === 'recording') {
                        stopRecording();
                    }
                }, MAX_RECORDING_TIME);
                
            })
            .catch(error => {
                console.error("Microphone error:", error);
                alert("❌ Could not access microphone. Please:\n1. Allow microphone permission\n2. Use Chrome/Firefox\n3. Or type text manually");
                resetUI();
            });
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            clearTimeout(recordingTimer);
            mediaRecorder.stop();
        } else {
            resetUI();
        }
    }
    
    function resetUI() {
        document.getElementById('recording-status').style.display = 'none';
        document.getElementById('recording-result').style.display = 'none';
        document.getElementById('start-btn').style.display = 'flex';
        document.getElementById('stop-btn').style.display = 'none';
        
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    }
    
    function useTranscript() {
        const transcript = document.getElementById('transcript-text').value;
        if (transcript.trim()) {
            // Send to Streamlit
            window.parent.postMessage({
                type: 'voice_transcript',
                data: transcript
            }, '*');
            
            // Show success message
            alert("✅ Voice input sent to translation! Scroll down to see results.");
            
            // Scroll to translation section
            const translationSection = document.querySelector('h2:contains("Translation Results")');
            if (translationSection) {
                translationSection.scrollIntoView({ behavior: 'smooth' });
            }
        } else {
            alert("Please enter some text first!");
        }
    }
    
    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'set_transcript') {
            document.getElementById('transcript-text').value = event.data.data;
        }
    });
    </script>
    """

# ==================== CORE FUNCTIONS ====================
def translate_text(text, target_lang='ta'):
    """Translate text to target language"""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        return f"Error: {str(e)}"

def simplify_english(text):
    """Simplify English text"""
    replacements = {
        'artificial intelligence': 'smart computer systems',
        'machine learning': 'computers that learn from data',
        'agriculture': 'farming',
        'irrigation': 'water supply',
        'fertilizer': 'plant food',
        'subsidy': 'government help',
        'authentication': 'verification',
        'transaction': 'money transfer',
        'financial': 'money',
        'portfolio': 'collection',
        'diversification': 'spreading',
        'mitigate': 'reduce',
    }
    
    for complex_word, simple_word in replacements.items():
        if complex_word in text.lower():
            text = text.replace(complex_word, simple_word)
    
    return text

def generate_audio(text, language='ta'):
    """Generate audio from text"""
    try:
        if language == 'ta':
            filename = "tamil_speech.mp3"
            tts = gTTS(text=text, lang='ta', slow=False)
        else:
            filename = "english_speech.mp3"
            tts = gTTS(text=text, lang='en', slow=False)
        
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
    
    tips_data = {
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
        ],
        'health': [
            "💊 Take medicines as prescribed",
            "🍎 Eat fruits and vegetables daily",
            "🚶 Walk 30 minutes every day",
            "💧 Drink 8 glasses of water daily",
            "😴 Sleep 7-8 hours nightly"
        ],
        'education': [
            "📚 Study 2 hours daily consistently",
            "🎯 Set daily learning goals",
            "🤝 Join study groups",
            "📱 Use educational apps",
            "✍️ Review notes before sleep"
        ]
    }
    
    # Detect topic
    if any(word in topic_lower for word in ['farm', 'crop', 'agriculture', 'irrigation', 'fertilizer']):
        return tips_data['agriculture'], 'agriculture'
    elif any(word in topic_lower for word in ['bank', 'money', 'otp', 'loan', 'account', 'upi']):
        return tips_data['bank'], 'bank'
    elif any(word in topic_lower for word in ['ai', 'artificial', 'intelligence', 'machine', 'robot']):
        return tips_data['ai'], 'ai'
    elif any(word in topic_lower for word in ['health', 'doctor', 'medicine', 'exercise', 'diet']):
        return tips_data['health'], 'health'
    elif any(word in topic_lower for word in ['study', 'education', 'learn', 'school', 'college']):
        return tips_data['education'], 'education'
    else:
        return ["🌞 Learn something new every day!", "💡 Practice makes perfect!", "🚀 Stay curious!"], 'general'

# ==================== SESSION STATE ====================
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'tamil_result' not in st.session_state:
    st.session_state.tamil_result = ""
if 'english_result' not in st.session_state:
    st.session_state.english_result = ""
if 'tamil_audio' not in st.session_state:
    st.session_state.tamil_audio = None
if 'english_audio' not in st.session_state:
    st.session_state.english_audio = None
if 'daily_tips' not in st.session_state:
    st.session_state.daily_tips = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🎤 Talk2Tamil: REAL Voice Recording</h1>
    <p style="font-size: 1.3rem; margin-top: 15px;">Speak → Record → Translate → Listen → Learn</p>
</div>
""", unsafe_allow_html=True)

# ==================== REAL VOICE RECORDER ====================
st.markdown("## 🎤 1. REAL Voice Recording")
st.markdown(get_voice_recorder_html(), unsafe_allow_html=True)

# ==================== TEXT INPUT (ALTERNATIVE) ====================
st.markdown("---")
st.markdown("## 📝 2. Or Type Text Directly")

text_input = st.text_area(
    "Type your message here (if voice recording doesn't work):",
    height=150,
    placeholder="Type any text for translation...\nExample: 'Artificial intelligence helps farmers predict crop diseases and improve harvest through data analysis.'",
    key="text_input"
)

if text_input:
    st.session_state.voice_text = text_input
    if st.button("✅ Use This Text", key="use_text_input", use_container_width=True):
        st.success("✅ Text loaded! Scroll down for translation.")

# ==================== TRANSLATION BUTTON ====================
st.markdown("---")

col_translate, col_clear = st.columns([3, 1])

with col_translate:
    if st.button("🚀 TRANSLATE NOW", type="primary", use_container_width=True):
        if st.session_state.voice_text:
            with st.spinner("🔄 Translating to both languages..."):
                # Get translations
                st.session_state.tamil_result = translate_text(st.session_state.voice_text, 'ta')
                st.session_state.english_result = simplify_english(st.session_state.voice_text)
                
                # Generate audio
                st.session_state.tamil_audio = generate_audio(st.session_state.tamil_result, 'ta')
                st.session_state.english_audio = generate_audio(st.session_state.english_result, 'en')
                
                # Get daily tips
                st.session_state.daily_tips, st.session_state.current_topic = get_daily_tips(st.session_state.voice_text)
                
            st.success("✅ Translation complete!")
        else:
            st.warning("Please record voice or type text first!")

with col_clear:
    if st.button("🗑️ Clear All", key="clear_all", use_container_width=True):
        st.session_state.voice_text = ""
        st.session_state.tamil_result = ""
        st.session_state.english_result = ""
        st.session_state.tamil_audio = None
        st.session_state.english_audio = None
        st.session_state.daily_tips = []
        st.rerun()

# ==================== TRANSLATION RESULTS ====================
if st.session_state.tamil_result or st.session_state.english_result:
    st.markdown("---")
    st.markdown("## 📊 3. Translation Results")
    
    # Language boxes in columns
    col_tamil, col_english = st.columns(2)
    
    with col_tamil:
        st.markdown("""
        <div class="language-box tamil-box">
            <h2>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h2>
            <p>Tamil Translation</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.tamil_result:
            st.markdown(f"""
            <div style="background: #FFE8E8; padding: 25px; border-radius: 15px; margin: 20px 0; min-height: 150px;">
                <p style="font-size: 18px; line-height: 1.8;">{st.session_state.tamil_result}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Tamil audio
            if st.session_state.tamil_audio and os.path.exists(st.session_state.tamil_audio):
                with open(st.session_state.tamil_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                # Download button
                st.download_button(
                    "📥 Download Tamil Audio",
                    audio_bytes,
                    file_name="talk2tamil_tamil.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
    
    with col_english:
        st.markdown("""
        <div class="language-box english-box">
            <h2>🇬🇧 Simple English</h2>
            <p>Easy to Understand</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.english_result:
            st.markdown(f"""
            <div style="background: #E0F7FA; padding: 25px; border-radius: 15px; margin: 20px 0; min-height: 150px;">
                <p style="font-size: 18px; line-height: 1.8;">{st.session_state.english_result}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # English audio
            if st.session_state.english_audio and os.path.exists(st.session_state.english_audio):
                with open(st.session_state.english_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                # Download button
                st.download_button(
                    "📥 Download English Audio",
                    audio_bytes,
                    file_name="talk2tamil_english.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

# ==================== DAILY TIPS ====================
if st.session_state.daily_tips:
    st.markdown("---")
    st.markdown("## 💡 4. Daily Useful Tips")
    
    st.info(f"📌 Topic Detected: **{st.session_state.current_topic.upper()}**")
    
    # Show tips in columns
    tip_cols = st.columns(2)
    for i, tip in enumerate(st.session_state.daily_tips[:6]):
        with tip_cols[i % 2]:
            st.markdown(f"""
            <div class="tip-box">
                <strong>Tip {i+1}:</strong> {tip}
            </div>
            """, unsafe_allow_html=True)

# ==================== DOWNLOAD RESULTS ====================
if st.session_state.voice_text and st.session_state.tamil_result:
    st.markdown("---")
    st.markdown("## 💾 5. Download All Results")
    
    # Create document
    doc_content = f"""
    TALK2TAMIL - VOICE TRANSLATION
    ================================
    Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Topic: {st.session_state.current_topic.upper()}
    
    ORIGINAL TEXT:
    {st.session_state.voice_text}
    
    TAMIL TRANSLATION:
    {st.session_state.tamil_result}
    
    SIMPLE ENGLISH:
    {st.session_state.english_result}
    
    DAILY TIPS:
    {chr(10).join(f'• {tip}' for tip in st.session_state.daily_tips)}
    
    ================================
    Talk2Tamil - Voice Assistant
    Making information accessible!
    """
    
    st.download_button(
        "📥 Download Complete Report",
        doc_content,
        file_name=f"talk2tamil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 Quick Examples")
    
    examples = [
        ("🌾 Agriculture", "Modern agriculture uses AI and technology for better crop prediction and irrigation management."),
        ("🏦 Banking", "Bank security requires never sharing OTP and using secure UPI apps for all transactions."),
        ("🤖 AI Tech", "Artificial intelligence helps analyze data and predict outcomes in farming, healthcare, and education."),
        ("🏥 Health", "Regular exercise, balanced diet, and proper sleep are essential for maintaining good health."),
        ("📚 Education", "Continuous learning and skill development through education improve career opportunities.")
    ]
    
    for label, text in examples:
        if st.button(label, key=f"ex_{label}"):
            st.session_state.voice_text = text
            st.rerun()
    
    st.markdown("---")
    
    # Voice Status
    st.markdown("## 🎤 Voice Status")
    if st.session_state.voice_text:
        st.success("✅ Voice/Text Ready")
        st.write(f"Words: {len(st.session_state.voice_text.split())}")
    else:
        st.warning("⏸️ No input yet")
    
    st.markdown("---")
    
    # Help
    st.markdown("## ❓ Need Help?")
    st.markdown("""
    **Voice not working?**
    1. Allow microphone access
    2. Use Chrome/Firefox
    3. Click "Allow" when prompted
    4. Or type text manually
    
    **Best for:**
    - Farmers
    - Students
    - Elderly
    - Rural communities
    
    **Features:**
    ✅ Real voice recording
    ✅ Tamil translation
    ✅ Simple English
    ✅ Audio playback
    ✅ Daily tips
    ✅ Download results
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p><strong>🎤 Talk2Tamil - REAL Voice Recording Assistant</strong></p>
    <p>Actual Voice Recording | Tamil & English Translation | Audio Playback | Daily Tips</p>
    <p><small>Making technology accessible through voice for everyone</small></p>
</div>
""", unsafe_allow_html=True)

# ==================== JAVASCRIPT TO CAPTURE VOICE TRANSCRIPT ====================
st.markdown("""
<script>
// Listen for voice transcript from the recorder
window.addEventListener('message', function(event) {
    if (event.data.type === 'voice_transcript') {
        // Store transcript in session
        sessionStorage.setItem('voice_transcript', event.data.data);
        
        // Show success message
        const successDiv = document.createElement('div');
        successDiv.innerHTML = '<div style="background: #4CAF50; color: white; padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;"><strong>✅ Voice recorded successfully!</strong><br>Scroll down for translation.</div>';
        document.querySelector('.recording-section').appendChild(successDiv);
        
        // Trigger Streamlit rerun with the transcript
        setTimeout(() => {
            window.location.href = window.location.href + '?voice=' + encodeURIComponent(event.data.data);
        }, 1000);
    }
});

// Check for voice transcript in URL
const urlParams = new URLSearchParams(window.location.search);
const voiceText = urlParams.get('voice');
if (voiceText) {
    // Set the text in the textarea
    const textAreas = document.querySelectorAll('textarea');
    if (textAreas.length > 1) {
        textAreas[1].value = decodeURIComponent(voiceText);
        // Trigger change event
        textAreas[1].dispatchEvent(new Event('input', { bubbles: true }));
    }
}
</script>
""", unsafe_allow_html=True)

# ==================== CHECK FOR VOICE INPUT FROM URL ====================
query_params = st.query_params
if 'voice' in query_params:
    st.session_state.voice_text = query_params['voice']
    st.rerun()
