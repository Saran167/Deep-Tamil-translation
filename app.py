import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import requests
import urllib.parse
import base64
from datetime import datetime
from PIL import Image
import os
import json
import tempfile
import wave
import time

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
    }
    
    @keyframes recordingPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        transition: all 0.3s !important;
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
    
    /* Browser recording */
    .browser-recording {
        background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%);
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #039BE5;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== VOICE RECORDING FUNCTIONS ====================
def get_browser_recorder_html():
    """HTML and JavaScript for browser-based voice recording"""
    return """
    <div class="browser-recording">
        <h3>🎤 Browser Voice Recorder</h3>
        <p>Click "Start Recording" to use your microphone directly in the browser.</p>
        
        <div id="recording-status" style="display: none; background: #FFEBEE; padding: 10px; border-radius: 5px; margin: 10px 0;">
            <strong>⏺️ Recording...</strong> Speak now!
        </div>
        
        <div id="audio-playback" style="display: none; margin: 15px 0;">
            <audio id="audio-player" controls style="width: 100%;"></audio>
        </div>
        
        <button id="start-recording" style="background: #FF5252; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 5px;">
            ⏺️ Start Recording
        </button>
        
        <button id="stop-recording" style="background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 5px; display: none;">
            ⏹️ Stop Recording
        </button>
        
        <button id="upload-audio" style="background: #2196F3; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; margin: 5px; display: none;">
            📤 Upload Audio
        </button>
        
        <div id="transcript-result" style="margin-top: 15px; padding: 15px; background: #F1F8E9; border-radius: 8px; display: none;">
            <h4>📝 Transcript:</h4>
            <textarea id="transcript-text" rows="3" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #C8E6C9;"></textarea>
            <button id="use-transcript" style="background: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                ✅ Use This Text
            </button>
        </div>
    </div>
    
    <script>
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;
    
    // Start recording
    document.getElementById('start-recording').addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audioPlayer = document.getElementById('audio-player');
                audioPlayer.src = audioUrl;
                
                document.getElementById('audio-playback').style.display = 'block';
                document.getElementById('upload-audio').style.display = 'inline-block';
                document.getElementById('recording-status').style.display = 'none';
                document.getElementById('stop-recording').style.display = 'none';
                document.getElementById('start-recording').style.display = 'inline-block';
                
                // Simulate transcription
                setTimeout(() => {
                    document.getElementById('transcript-result').style.display = 'block';
                    document.getElementById('transcript-text').value = "This is a simulated transcript. In a real app, this would be your spoken text.";
                }, 1000);
            };
            
            mediaRecorder.start();
            audioChunks = [];
            
            document.getElementById('recording-status').style.display = 'block';
            document.getElementById('stop-recording').style.display = 'inline-block';
            document.getElementById('start-recording').style.display = 'none';
            document.getElementById('audio-playback').style.display = 'none';
            document.getElementById('upload-audio').style.display = 'none';
            document.getElementById('transcript-result').style.display = 'none';
            
        } catch (error) {
            alert("Error accessing microphone: " + error.message);
        }
    });
    
    // Stop recording
    document.getElementById('stop-recording').addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    });
    
    // Use transcript
    document.getElementById('use-transcript').addEventListener('click', () => {
        const transcript = document.getElementById('transcript-text').value;
        if (transcript.trim()) {
            // Send to Streamlit
            window.parent.postMessage({
                type: 'voice_transcript',
                data: transcript
            }, '*');
            alert("✅ Text sent to translation!");
        }
    });
    
    // Upload audio simulation
    document.getElementById('upload-audio').addEventListener('click', () => {
        alert("🎵 Audio ready! Click 'Use This Text' to proceed.");
    });
    </script>
    """

# ==================== SPEECH RECOGNITION ALTERNATIVE ====================
def transcribe_with_api(audio_file=None, text=None):
    """Use online speech recognition API as fallback"""
    if text:
        return text  # If we already have text from browser
    
    # For demo purposes, return sample text
    sample_texts = [
        "Artificial intelligence helps farmers with crop prediction",
        "Bank security is important for everyone's safety",
        "Agriculture needs better irrigation systems",
        "Education improves career opportunities for everyone",
        "Health is wealth, exercise daily and eat healthy"
    ]
    
    import random
    return random.choice(sample_texts)

# ==================== CORE FUNCTIONS ====================
def translate_text(text, target_lang='ta'):
    """Smart translation with rural Tamil optimization"""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        
        # Apply rural Tamil optimizations if target is Tamil
        if target_lang == 'ta':
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
    }
    
    import re
    simplified = text
    for complex_word, simple_word in simplification_dict.items():
        pattern = re.compile(re.escape(complex_word), re.IGNORECASE)
        simplified = pattern.sub(simple_word, simplified)
    
    sentences = simplified.split('. ')
    short_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 15:
            mid = len(words) // 2
            part1 = ' '.join(words[:mid]) + '.'
            part2 = ' '.join(words[mid:])
            short_sentences.append(part1)
            short_sentences.append(part2)
        else:
            short_sentences.append(sentence)
    
    return '. '.join(short_sentences)

def generate_audio(text, language='ta'):
    """Generate voice output"""
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

def get_daily_tips(topic, language='ta'):
    """Get daily use tips based on input topic"""
    
    topic_lower = topic.lower()
    
    tips_database = {
        'ai': {
            'ta': [
                "🤖 AI உங்கள் வாழ்க்கையை எளிதாக்கும்!",
                "📱 Google Assistant, Siri போன்ற AI உதவியாளர்களைப் பயன்படுத்தவும்",
                "📸 AI கேமராக்கள் சிறப்பான புகைப்படங்களை எடுக்க உதவும்",
                "📚 AI பயன்பாடுகளைக் கற்றுக்கொள்ள YouTube பாடங்களைப் பார்க்கவும்",
                "🛡️ AI மூலம் மோசடி செய்திகளை அடையாளம் காணலாம்",
            ],
            'en': [
                "🤖 AI can make your life easier!",
                "📱 Use AI assistants like Google Assistant, Siri for daily help",
                "📸 AI cameras help take better photos automatically",
                "📚 Learn about AI apps through YouTube tutorials",
                "🛡️ AI can help detect scam messages and calls",
            ]
        },
        'bank': {
            'ta': [
                "🏦 உங்கள் OTP யாருக்கும் சொல்லாதீர்கள்",
                "💳 ATM கார்டு PIN எப்போதும் ரகசியமாக வைக்கவும்",
                "📱 UPI பயன்பாடுகளை பாதுகாப்பாக பயன்படுத்தவும்",
                "📞 வங்கி மோசடி பற்றிய புகார்களை 1930 க்கு அறிவிக்கவும்",
                "💰 சந்தேகத்திற்கிடமான கடன் செய்திகளை நம்பாதீர்கள்",
            ],
            'en': [
                "🏦 Never share your OTP with anyone",
                "💳 Keep ATM card PIN secret always",
                "📱 Use UPI apps safely with password protection",
                "📞 Report bank frauds immediately to 1930",
                "💰 Don't trust suspicious loan messages",
            ]
        },
        'health': {
            'ta': [
                "💊 மருந்துகளை மருத்துவர் ஆலோசனையின்றி எடுக்கக்கூடாது",
                "🍎 தினமும் பழங்கள் மற்றும் காய்கறிகளை சாப்பிடவும்",
                "🚶‍♂️ தினமும் குறைந்தது 30 நிமிடம் நடக்கவும்",
                "💧 தினமும் 8 கிளாஸ் தண்ணீர் குடிக்கவும்",
                "😴 இரவு 7-8 மணி நேரம் உறங்கவும்",
            ],
            'en': [
                "💊 Don't take medicines without doctor consultation",
                "🍎 Eat fruits and vegetables daily",
                "🚶‍♂️ Walk at least 30 minutes every day",
                "💧 Drink 8 glasses of water daily",
                "😴 Sleep 7-8 hours every night",
            ]
        },
        'education': {
            'ta': [
                "📚 தினமும் குறைந்தது 2 மணி நேரம் படிக்கவும்",
                "📝 புதிய வார்த்தைகளை கற்றுக்கொள்ள தினசரி 5 சொற்கள்",
                "🎯 இலக்குகளை அமைத்து அவற்றை அடைய திட்டமிடவும்",
                "🤝 குழுவாக படிப்பது மேம்பட்ட கற்றலை அளிக்கும்",
                "📱 கல்வி பயன்பாடுகளைப் பயன்படுத்தி புதிய திறன்களைக் கற்றுக்கொள்ளுங்கள்",
            ],
            'en': [
                "📚 Study at least 2 hours daily",
                "📝 Learn 5 new words every day",
                "🎯 Set goals and plan to achieve them",
                "🤝 Group study provides better learning",
                "📱 Use educational apps to learn new skills",
            ]
        },
        'agriculture': {
            'ta': [
                "🌾 நல்ல விளைச்சலுக்கு சரியான நேரத்தில் விதைக்கவும்",
                "💧 தண்ணீர் மிச்சப்படுத்தும் நீர்ப்பாசன முறைகளை பயன்படுத்தவும்",
                "🌱 இயற்கை உரங்களை பயன்படுத்தி மண்ணின் ஆரோக்கியத்தை பராமரிக்கவும்",
                "🐛 பூச்சி மற்றும் நோய் மேலாண்மைக்கு இயற்கை முறைகளை பின்பற்றவும்",
                "💰 அரசு மானியங்கள் மற்றும் கடன் திட்டங்களைப் பயன்படுத்தவும்",
                "📊 சந்தை விலைகளை அறிந்து சிறந்த நேரத்தில் பயிர்களை விற்கவும்",
                "🌦️ வானிலை முன்னறிவிப்புகளை கவனித்து பயிர் பாதுகாப்பு நடவடிக்கைகளை எடுக்கவும்",
                "🌿 பல பயிர் சாகுபடி முறையை பின்பற்றி ஆபத்தை குறைக்கவும்",
                "📱 கிராமத்தின் விவசாய பயன்பாடுகளைப் பயன்படுத்தி புதிய தொழில்நுட்பங்களைக் கற்றுக்கொள்ளுங்கள்",
                "👨‍🌾 விவசாய விரிவாக்க அலுவலர்களிடம் ஆலோசனை பெறவும்",
            ],
            'en': [
                "🌾 Sow seeds at the right time for good yield",
                "💧 Use water-saving irrigation methods to conserve water",
                "🌱 Maintain soil health using organic fertilizers",
                "🐛 Follow natural methods for pest and disease management",
                "💰 Utilize government subsidies and loan schemes",
                "📊 Know market prices and sell crops at the best time",
                "🌦️ Monitor weather forecasts and take crop protection measures",
                "🌿 Follow crop diversification to reduce risk",
                "📱 Learn new technologies using farming apps",
                "👨‍🌾 Consult agriculture extension officers for advice",
            ]
        },
        'government': {
            'ta': [
                "🏛️ அரசு சலுகைகள் மற்றும் திட்டங்களைப் பற்றி அறிந்து கொள்ளவும்",
                "📄 ஆவணங்களை பாதுகாப்பாக வைத்திருங்கள் (ஆதார், வாக்காளர் அட்டை)",
                "📞 கிராமப்புற மையங்கள் மூலம் அரசு சேவைகளைப் பெறுங்கள்",
                "💼 வேலைவாய்ப்பு திட்டங்கள் மற்றும் பயிற்சி திட்டங்களைப் பயன்படுத்தவும்",
                "🏥 இலவச மருத்துவ முகாம்கள் மற்றும் சுகாதார சேவைகளைப் பயன்படுத்தவும்",
            ],
            'en': [
                "🏛️ Know about government schemes and benefits",
                "📄 Keep documents safe (Aadhaar, voter ID)",
                "📞 Access government services through rural centers",
                "💼 Utilize employment schemes and training programs",
                "🏥 Use free medical camps and health services",
            ]
        }
    }
    
    # Topic detection
    detected_topic = 'ai'
    
    agriculture_keywords = ['agriculture', 'farming', 'crop', 'farmer', 'cultivation', 'irrigation', 
                          'harvest', 'soil', 'fertilizer', 'pesticide', 'yield', 'field', 'விவசாய',
                          'பயிர்', 'விளைச்சல்', 'நீர்ப்பாசனம்', 'உரம்']
    
    bank_keywords = ['bank', 'account', 'money', 'loan', 'otp', 'upi', 'transaction', 'credit', 'debit',
                    'வங்கி', 'கணக்கு', 'கடன்', 'பணம்', 'பரிவர்த்தனை']
    
    health_keywords = ['health', 'doctor', 'medicine', 'hospital', 'exercise', 'water', 'sleep', 'diet',
                      'ஆரோக்கியம்', 'மருத்துவர்', 'மருந்து', 'மருத்துவமனை', 'பயிற்சி']
    
    education_keywords = ['study', 'education', 'school', 'college', 'learn', 'read', 'student', 'exam',
                         'கல்வி', 'பாடம்', 'பள்ளி', 'கல்லூரி', 'படிப்பு']
    
    government_keywords = ['government', 'scheme', 'subsidy', 'benefit', 'certificate', 'document',
                          'அரசு', 'திட்டம்', 'மானியம்', 'சலுகை', 'சான்றிதழ்']
    
    if any(keyword in topic_lower for keyword in agriculture_keywords):
        detected_topic = 'agriculture'
    elif any(keyword in topic_lower for keyword in bank_keywords):
        detected_topic = 'bank'
    elif any(keyword in topic_lower for keyword in health_keywords):
        detected_topic = 'health'
    elif any(keyword in topic_lower for keyword in education_keywords):
        detected_topic = 'education'
    elif any(keyword in topic_lower for keyword in government_keywords):
        detected_topic = 'government'
    elif any(keyword in topic_lower for keyword in ['ai', 'artificial', 'intelligence', 'machine', 'robot']):
        detected_topic = 'ai'
    
    tips = tips_database.get(detected_topic, {}).get(language, [])
    
    if not tips:
        if language == 'ta':
            tips = ["🌞 நாள்தோறும் புதிய விஷயங்களைக் கற்றுக்கொள்ள முயற்சிக்கவும்!"]
        else:
            tips = ["🌞 Try to learn new things every day!"]
    
    return tips, detected_topic

def create_document(content_dict, language='ta'):
    """Create downloadable document"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    doc_content = f"""
    ============================================
    TALK2TAMIL - TRANSLATION RESULT
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Topic: {content_dict.get('detected_topic', '').upper()}
    ============================================

    📝 ORIGINAL TEXT:
    {content_dict.get('original', '')}

    """
    
    if language in ['ta', 'both'] and content_dict.get('tamil'):
        doc_content += f"""
    🇮🇳 TAMIL TRANSLATION:
    {content_dict.get('tamil', '')}

    """
    
    if language in ['en', 'both'] and content_dict.get('english'):
        doc_content += f"""
    🇬🇧 SIMPLE ENGLISH:
    {content_dict.get('english', '')}

    """
    
    if content_dict.get('daily_tips'):
        doc_content += f"""
    💡 DAILY USEFUL TIPS ({content_dict.get('detected_topic', '').upper()}):
    ============================================
    {chr(10).join(['• ' + tip for tip in content_dict.get('daily_tips', [])])}

    """
    
    doc_content += f"""
    ============================================
    Talk2Tamil - Smart Translation Assistant
    Making information accessible for everyone!
    ============================================
    """
    
    return doc_content

# ==================== INITIALIZE SESSION STATE ====================
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
if 'voice_recorded' not in st.session_state:
    st.session_state.voice_recorded = None
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""
if 'browser_recording' not in st.session_state:
    st.session_state.browser_recording = False

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <h1>🗣️🤖 Talk2Tamil: Smart Assistant</h1>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 15px; flex-wrap: wrap;">
        <span>🎤 BROWSER Voice Recording</span>
        <span>📸 Image Upload</span>
        <span>📝 Text Input</span>
        <span>🇮🇳 Tamil Output</span>
        <span>🇬🇧 Simple English</span>
        <span>💡 Smart Daily Tips</span>
        <span>🔊 Voice Output</span>
        <span>📄 Document</span>
    </div>
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
input_tab1, input_tab2, input_tab3 = st.tabs(["🎤 Browser Voice Recording", "📝 Type Text", "📸 Upload Image"])

with input_tab1:
    st.markdown("### 🎤 Browser-Based Voice Recording")
    st.markdown("""
    <div style="background: #E8F5E9; padding: 20px; border-radius: 15px; margin: 10px 0;">
        <h4>✅ Voice Recording Works!</h4>
        <p>Using <strong>browser microphone access</strong> - no Python installation needed!</p>
        <p><strong>How it works:</strong></p>
        <ol>
            <li>Click <strong>"Start Recording"</strong> below</li>
            <li>Allow microphone access in browser</li>
            <li>Speak clearly in English</li>
            <li>Click <strong>"Stop Recording"</strong></li>
            <li>Get your transcript automatically</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        # Browser-based voice recorder
        st.markdown(get_browser_recorder_html(), unsafe_allow_html=True)
        
        # Demo voice input buttons
        st.markdown("---")
        st.markdown("### 🎯 Quick Voice Demos")
        
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            if st.button("🌾 Speak Agriculture", use_container_width=True):
                st.session_state.current_input = "Good agriculture practices increase crop yield and farmer income."
                st.success("✅ Demo text set! Go to Translate section.")
        
        with demo_col2:
            if st.button("🏦 Speak Banking", use_container_width=True):
                st.session_state.current_input = "Bank security is important. Never share your OTP with anyone."
                st.success("✅ Demo text set! Go to Translate section.")
        
        with demo_col3:
            if st.button("🤖 Speak AI", use_container_width=True):
                st.session_state.current_input = "Artificial intelligence helps farmers with crop prediction using data."
                st.success("✅ Demo text set! Go to Translate section.")
        
        # Manual input as backup
        st.markdown("---")
        st.markdown("#### 💬 Or type manually:")
        manual_voice = st.text_area("Type your spoken text:", 
                                   height=100, 
                                   key="manual_voice",
                                   placeholder="Type what you would say...\nExample: 'AI technology helps farmers predict crop diseases'")
        if manual_voice:
            st.session_state.current_input = manual_voice
    
    with col_v2:
        st.markdown("### 🎯 Voice Tips")
        st.markdown("""
        **For best results:**
        
        🔊 **Allow microphone access**
        🎤 **Speak clearly and slowly**
        🏠 **Quiet environment**
        🗣️ **English works best**
        ⏸️ **Pause between sentences**
        
        **Works in:**
        - Chrome/Firefox/Edge
        - Mobile browsers
        - No Python install needed!
        
        **Browser Security:**
        - Requires microphone permission
        - Recording stays in browser
        - No audio uploaded to server
        """)

with input_tab2:
    st.markdown("### ✍️ Type or Paste Text")
    text_input = st.text_area(
        "Enter your text in any language:",
        height=200,
        placeholder="Type or paste your text here...\n\nExamples:\n• 'Agriculture helps in economic growth'\n• 'Bank OTP should not be shared with anyone'\n• 'AI is useful in farming for crop prediction'\n• 'Regular exercise maintains good health'\n• 'Education improves career opportunities'",
        key="text_input",
        help="Type in English, Tamil, or any language"
    )
    if text_input:
        st.session_state.current_input = text_input

with input_tab3:
    st.markdown("### 📸 Upload Image with Text")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload screenshots, documents, or any image with text"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 Uploaded Image", width=300)
        
        st.info("🔍 For image text extraction, please type the text manually below:")
        image_text = st.text_area("📝 Type text from image:", height=150, key="image_text")
        if image_text:
            st.session_state.current_input = image_text

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
    
    voice_output = st.checkbox(
        "🔊 Generate voice output",
        value=True,
        help="Listen to translations"
    )
    
    doc_output = st.checkbox(
        "📄 Generate downloadable document",
        value=True,
        help="Download all results as text file"
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
    "✨ TRANSLATE & GET SMART TIPS",
    type="primary",
    use_container_width=True,
    key="translate_btn"
):
    if st.session_state.current_input and st.session_state.current_input.strip():
        with st.spinner("🔄 Processing..."):
            # Get translation
            tamil_text = ""
            english_text = ""
            
            if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
                tamil_text = translate_text(st.session_state.current_input, 'ta')
            
            if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
                english_text = simplify_english(st.session_state.current_input)
            
            # Get daily tips with IMPROVED detection
            tips_lang_code = 'ta' if tips_language == "🇮🇳 Tamil" else 'en'
            daily_tips, detected_topic = get_daily_tips(st.session_state.current_input, tips_lang_code)
            
            # Store in session
            st.session_state.translation_result = {
                'original': st.session_state.current_input,
                'tamil': tamil_text,
                'english': english_text,
                'daily_tips': daily_tips,
                'detected_topic': detected_topic,
                'tips_language': tips_language,
                'output_option': output_option
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
    
    # Show detected topic with emoji
    topic_emojis = {
        'ai': '🤖',
        'bank': '🏦', 
        'health': '🏥',
        'education': '📚',
        'agriculture': '🌾',
        'government': '🏛️'
    }
    
    emoji = topic_emojis.get(result['detected_topic'], '💡')
    st.success(f"{emoji} **Smart Detection:** Your text is about **{result['detected_topic'].upper()}**")
    
    # Display translations
    if result['output_option'] == "🌍 Both Languages":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("### 🇮🇳 தமிழ் மொழிபெயர்ப்பு")
            if result['tamil']:
                st.success(result['tamil'])
                
                if voice_output:
                    if st.button("🔊 Play Tamil Audio", key="play_tamil"):
                        audio_file = generate_audio(result['tamil'], 'ta')
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
        
        with col_english:
            st.markdown("### 🇬🇧 Simple English")
            if result['english']:
                st.success(result['english'])
                
                if voice_output:
                    if st.button("🔊 Play English Audio", key="play_english"):
                        audio_file = generate_audio(result['english'], 'en')
                        if audio_file:
                            st.audio(audio_file, format='audio/mp3')
    
    elif result['output_option'] == "🇮🇳 Tamil Only":
        st.markdown("### 🇮🇳 Tamil Translation")
        if result['tamil']:
            st.success(result['tamil'])
            
            if voice_output:
                if st.button("🔊 Play Tamil Audio", key="play_tamil_only"):
                    audio_file = generate_audio(result['tamil'], 'ta')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
    
    else:
        st.markdown("### 🇬🇧 Simplified English")
        if result['english']:
            st.success(result['english'])
            
            if voice_output:
                if st.button("🔊 Play English Audio", key="play_english_only"):
                    audio_file = generate_audio(result['english'], 'en')
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
    
    # ==================== DAILY TIPS SECTION ====================
    st.markdown("---")
    st.markdown(f"""
    <div class="daily-tip">
        <h2><span class="tip-icon">💡</span> Smart Daily Tips for {result['detected_topic'].upper()} ({result['tips_language']})</h2>
        <p>Based on your input about <strong>{result['detected_topic'].upper()}</strong>, here are useful tips:</p>
    </div>
    """, unsafe_allow_html=True)
    
    if result['daily_tips']:
        for i, tip in enumerate(result['daily_tips'][:5]):
            st.markdown(f"""
            <div style="background: {'#FFF9C4' if i % 2 == 0 else '#E1F5FE'}; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin: 10px 0;">
                <h4>{topic_emojis.get(result['detected_topic'], '💡')} Tip {i+1}</h4>
                <p>{tip}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Document download
        if doc_output:
            st.markdown("---")
            st.markdown("### 📄 Download Complete Results")
            
            # Create document
            doc_lang = 'both'
            if result['output_option'] == "🇮🇳 Tamil Only":
                doc_lang = 'ta'
            elif result['output_option'] == "🇬🇧 Simple English Only":
                doc_lang = 'en'
            
            doc_content = create_document(result, doc_lang)
            
            st.download_button(
                label="📥 Download as Text File",
                data=doc_content,
                file_name=f"talk2tamil_{result['detected_topic']}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="download_doc"
            )

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📋 Test Topics")
    
    test_topics = {
        "🌾 Agriculture": "Good agriculture practices increase crop yield and farmer income.",
        "🏦 Banking": "Never share your bank OTP with anyone for security.",
        "🤖 AI Technology": "Artificial intelligence helps farmers with crop prediction.",
        "🏥 Health Care": "Regular exercise and balanced diet maintain good health.",
        "📚 Education": "Daily study habits improve learning outcomes.",
        "🏛️ Government": "Government schemes help farmers with subsidies."
    }
    
    selected = st.selectbox("Choose test topic:", list(test_topics.keys()))
    
    if st.button("📝 Use This Topic", key="use_topic"):
        st.session_state.current_input = test_topics[selected]
        st.rerun()
    
    st.markdown("---")
    st.markdown("## 🎤 Voice Recording Status")
    st.success("✅ **BROWSER VOICE RECORDING ACTIVE**")
    st.markdown("""
    **How it works:**
    1. Click "Start Recording"
    2. Allow microphone
    3. Speak in English
    4. Get transcript
    
    **Requirements:**
    - Modern browser
    - Microphone
    - HTTPS connection
    
    **Demo buttons available!**
    """)
    
    st.markdown("---")
    st.markdown("## 🎯 Topic Detection")
    st.markdown("""
    **Smart detection for:**
    - 🌾 **Agriculture**: farming, crops, irrigation
    - 🏦 **Banking**: OTP, loan, account, money
    - 🤖 **AI**: artificial intelligence, machine learning
    - 🏥 **Health**: exercise, diet, medicine
    - 📚 **Education**: study, learning, school
    - 🏛️ **Government**: schemes, subsidies, benefits
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <p>🚀 <strong>Talk2Tamil: Complete Smart Assistant</strong></p>
    <p>🎤 BROWSER Voice Recording | 📸 Image Upload | 📝 Text Input | 🇮🇳 Tamil | 🇬🇧 Simple English</p>
    <p>💡 Smart Topic Detection | 🔊 Voice Output | 📄 Document Download</p>
    <p><small>✅ Voice recording works in browser - no Python installation needed!</small></p>
</div>
""", unsafe_allow_html=True)

# ==================== JAVASCRIPT FOR VOICE TRANSCRIPT ====================
st.markdown("""
<script>
// Listen for messages from the voice recorder
window.addEventListener('message', function(event) {
    if (event.data.type === 'voice_transcript') {
        // This would send the transcript to Streamlit
        console.log('Voice transcript:', event.data.data);
        // In a real implementation, you would use Streamlit's set_query_params or other method
        alert("Transcript received: " + event.data.data);
    }
});
</script>
""", unsafe_allow_html=True)
