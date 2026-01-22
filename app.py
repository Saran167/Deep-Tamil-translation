import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import io
import base64
from datetime import datetime
import os
import requests
import urllib.parse
import json
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talk2Tamil - Voice & Chat Assistant",
    page_icon="🗣️🤖",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        color: #1E3A8A;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .section-header {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .language-box {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .chatbot-box {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .voice-box {
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .record-btn {
        background: linear-gradient(90deg, #EF4444 0%, #DC2626 100%) !important;
        color: white !important;
    }
    .stop-btn {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
    }
    .chat-message-user {
        background-color: #E0F2FE;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #3B82F6;
    }
    .chat-message-bot {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #F59E0B;
    }
    .tab-content {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_translation' not in st.session_state:
    st.session_state.current_translation = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'recorded_audio' not in st.session_state:
    st.session_state.recorded_audio = None

# ==================== FUNCTIONS ====================

# --- Voice Recording Simulation ---
def start_recording():
    """Simulate starting voice recording"""
    st.session_state.is_recording = True
    st.session_state.recorded_audio = None

def stop_recording():
    """Simulate stopping voice recording"""
    st.session_state.is_recording = False
    # Simulate processing - in real app, this would process actual audio
    time.sleep(1)
    st.session_state.recorded_audio = "simulated_audio.mp3"
    return "This is a simulated voice input. In real implementation, this would convert speech to text."

# --- Simplified Voice Input using Browser API ---
def voice_input_html():
    """HTML/JavaScript for browser voice recording"""
    return """
    <script>
    function startRecording() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser doesn't support speech recognition. Try Chrome.");
            return;
        }
        
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'ta-IN'; // Tamil India
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('voice-input').value = transcript;
            document.getElementById('voice-form').submit();
        };
        
        recognition.start();
    }
    </script>
    
    <button onclick="startRecording()" style="
        background: linear-gradient(90deg, #EF4444 0%, #DC2626 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 10px 0;
    ">
        🎤 Start Speaking (Tamil/English)
    </button>
    
    <form id="voice-form">
        <input type="hidden" id="voice-input" name="voice_text">
    </form>
    """

# --- Translation Functions ---
def translate_to_tamil(text):
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        return translator.translate(text)
    except:
        return text

def simplify_english(text):
    """Comprehensive English simplifier"""
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
    }
    
    # Simple word replacement
    for complex_word, simple_word in simplification_dict.items():
        if complex_word in text.lower():
            text = text.lower().replace(complex_word, simple_word)
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    
    return text

# --- Audio Generation ---
def generate_audio(text, language='ta', filename="audio.mp3"):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        return filename
    except:
        return None

# --- Chatbot Functions ---
class SimpleChatbot:
    def __init__(self):
        self.context = ""
        self.qa_pairs = {
            # General questions about translation
            "what is this": "This is a translation of your text.",
            "translate again": "I can translate it again for you.",
            "explain": "Let me explain the translation...",
            
            # Tamil specific
            "tamil meaning": "This is the Tamil translation of your text.",
            "speak tamil": "I will speak the Tamil translation.",
            
            # English specific
            "simple english": "This is simplified English for easy understanding.",
            "explain english": "The English version uses simpler words.",
        }
    
    def set_context(self, original_text, tamil_translation, english_translation):
        """Set the current document context for the chatbot"""
        self.context = f"""
        Original Text: {original_text}
        Tamil Translation: {tamil_translation}
        Simple English: {english_translation}
        """
    
    def answer_question(self, question, ask_in_tamil=False):
        """Answer questions based on context"""
        
        # If question is in Tamil, translate to English first
        question_lower = question.lower()
        
        # Check for keywords
        if "what is" in question_lower or "explain" in question_lower:
            if ask_in_tamil:
                return "இது உங்கள் உரையின் மொழிபெயர்ப்பு ஆகும். இன்னும் விளக்கத்திற்கு கேளுங்கள்."
            else:
                return "This is a translation of your text. Please ask more specific questions."
        
        elif "tamil" in question_lower:
            if ask_in_tamil:
                return "இது தமிழ் மொழிபெயர்ப்பு. மேலும் விளக்கங்களுக்கு கேளுங்கள்."
            else:
                return "This is the Tamil translation. Ask me to explain any part."
        
        elif "english" in question_lower or "simple" in question_lower:
            if ask_in_tamil:
                return "இது எளிய ஆங்கிலம். கடினமான சொற்களை எளிதாக்கியுள்ளோம்."
            else:
                return "This is simplified English. Complex words have been made easier."
        
        elif "voice" in question_lower or "speak" in question_lower:
            if ask_in_tamil:
                return "குரல் வெளியீட்டை கேட்க பிளே பொத்தானை அழுத்தவும்."
            else:
                return "Press the play button to hear the voice output."
        
        elif "download" in question_lower or "pdf" in question_lower:
            if ask_in_tamil:
                return "PDF பதிவிறக்க பொத்தானை கிளிக் செய்யவும்."
            else:
                return "Click the download PDF button to save the document."
        
        else:
            if ask_in_tamil:
                return "மன்னிக்கவும், இந்த கேள்விக்கு பதில் தெரியவில்லை. வேறு கேள்வி கேளுங்கள்."
            else:
                return "I'm sorry, I don't know the answer to that question. Please ask something else."

# Initialize chatbot
chatbot = SimpleChatbot()

# ==================== MAIN APP LAYOUT ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>🗣️🤖 Talk2Tamil: Voice & Chat Assistant</h1>
    <p>🎤 Voice Input | 🌍 Translation | 🤖 Q&A Chatbot | 🔊 Voice Output | 📄 Documents</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different modes
tab1, tab2, tab3 = st.tabs(["🎤 Voice Input", "📝 Text/Image Input", "🤖 Chat Assistant"])

# ==================== TAB 1: VOICE INPUT ====================
with tab1:
    st.markdown("<div class='section-header'><h3>🎤 Speak in Tamil or English</h3></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='voice-box'>
            <h4>🎙️ Voice Input Instructions</h4>
            <p>1. Click the record button below<br>
            2. Speak in Tamil or English<br>
            3. Click stop when finished<br>
            4. Your speech will be converted to text</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice recording buttons
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            if st.button("🔴 Start Recording", key="start_rec", use_container_width=True):
                start_recording()
        
        with col_rec2:
            if st.button("⏹️ Stop Recording", key="stop_rec", use_container_width=True):
                voice_text = stop_recording()
                st.session_state.voice_input_text = voice_text
                st.success("✅ Voice recorded! Text extracted below.")
        
        # Show recording status
        if st.session_state.is_recording:
            st.markdown("""
            <div style='text-align: center; padding: 2rem; background: #FEE2E2; border-radius: 10px;'>
                <h3>🔴 RECORDING...</h3>
                <p>Speak now in Tamil or English</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display voice input text
        if 'voice_input_text' in st.session_state:
            st.text_area("🎤 Your Voice Input:", st.session_state.voice_input_text, height=150)
            
            # Use this text for translation
            if st.button("✨ Translate Voice Input", type="primary"):
                st.session_state.current_translation = {
                    'original': st.session_state.voice_input_text,
                    'tamil': translate_to_tamil(st.session_state.voice_input_text),
                    'english': simplify_english(st.session_state.voice_input_text)
                }
                st.rerun()
    
    with col2:
        st.markdown("### 🎯 Language Tips")
        st.markdown("""
        **For best results:**
        
        **தமிழ் (Tamil):**
        - Speak clearly
        - Normal speed
        - No background noise
        
        **English:**
        - Clear pronunciation
        - Medium pace
        - Complete sentences
        """)
        
        # Browser-based voice input (alternative)
        st.markdown("---")
        st.markdown("### 🌐 Browser Voice Input")
        st.markdown("*(For Chrome users only)*")
        
        # Inject HTML/JS for browser voice
        components.html(voice_input_html(), height=200)

# ==================== TAB 2: TEXT/IMAGE INPUT ====================
with tab2:
    st.markdown("<div class='section-header'><h3>📝 Type, Paste, or Upload</h3></div>", unsafe_allow_html=True)
    
    col_input, col_settings = st.columns([2, 1])
    
    with col_input:
        input_method = st.radio(
            "✨ Choose input method:",
            ["✍️ Type/Paste Text", "📁 Upload File (TXT/DOCX/PDF)"]
        )
        
        input_text = ""
        
        if input_method == "✍️ Type/Paste Text":
            input_text = st.text_area(
                "Enter text in any language:",
                height=200,
                placeholder="Type or paste your text here...\nYou can type in English, Tamil, Hindi, etc.",
                key="text_input"
            )
        
        else:  # Upload File
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['txt', 'docx', 'pdf'],
                help="Supports: .txt, .docx, .pdf files"
            )
            if uploaded_file:
                if uploaded_file.name.endswith('.txt'):
                    input_text = uploaded_file.read().decode()
                elif uploaded_file.name.endswith('.docx'):
                    import docx
                    doc = docx.Document(uploaded_file)
                    input_text = "\n".join([para.text for para in doc.paragraphs])
                elif uploaded_file.name.endswith('.pdf'):
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    input_text = ""
                    for page in pdf_reader.pages:
                        input_text += page.extract_text()
                
                st.text_area("📄 Extracted Text:", input_text, height=150)
    
    with col_settings:
        st.markdown("### ⚙️ Output Settings")
        
        output_option = st.radio(
            "🎯 Select output:",
            ["🇮🇳 Tamil Only", "🇬🇧 Simple English Only", "🌍 Both Languages"]
        )
        
        st.markdown("---")
        
        voice_option = st.checkbox("🔊 Generate voice output", value=True)
        doc_option = st.checkbox("📄 Create downloadable file", value=True)
        
        st.markdown("---")
        
        process_btn = st.button(
            "✨ TRANSLATE NOW",
            type="primary",
            use_container_width=True,
            key="translate_btn"
        )
    
    # Process translation
    if process_btn and input_text.strip():
        with st.spinner("🔄 Processing translation..."):
            tamil_translation = ""
            english_translation = ""
            
            if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
                tamil_translation = translate_to_tamil(input_text)
            
            if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
                english_translation = simplify_english(input_text)
            
            # Store in session
            st.session_state.current_translation = {
                'original': input_text,
                'tamil': tamil_translation,
                'english': english_translation
            }
            
            # Set chatbot context
            chatbot.set_context(input_text, tamil_translation, english_translation)
            
            # Add to history
            st.session_state.translation_history.append({
                'time': datetime.now().strftime("%H:%M:%S"),
                'input': input_text[:50] + "...",
                'output': output_option
            })
    
    # Display translation results
    if st.session_state.current_translation:
        st.markdown("---")
        st.markdown("## 📊 Translation Results")
        
        if output_option == "🌍 Both Languages":
            col_tamil, col_english = st.columns(2)
            
            with col_tamil:
                st.markdown("""
                <div class="language-box">
                    <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
                </div>
                """, unsafe_allow_html=True)
                st.write(st.session_state.current_translation['tamil'])
                
                if voice_option:
                    audio_file = generate_audio(
                        st.session_state.current_translation['tamil'], 
                        'ta',
                        "tamil_output.mp3"
                    )
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        st.success("✅ Tamil audio ready")
            
            with col_english:
                st.markdown("""
                <div class="language-box">
                    <h3>🇬🇧 Simple English</h3>
                </div>
                """, unsafe_allow_html=True)
                st.write(st.session_state.current_translation['english'])
                
                if voice_option:
                    audio_file = generate_audio(
                        st.session_state.current_translation['english'],
                        'en',
                        "english_output.mp3"
                    )
                    if audio_file:
                        st.audio(audio_file, format='audio/mp3')
                        st.success("✅ English audio ready")
        
        elif output_option == "🇮🇳 Tamil Only":
            st.markdown("""
            <div class="language-box">
                <h3>🇮🇳 Tamil Translation</h3>
                <p>{}</p>
            </div>
            """.format(st.session_state.current_translation['tamil']), unsafe_allow_html=True)
            
            if voice_option:
                audio_file = generate_audio(
                    st.session_state.current_translation['tamil'],
                    'ta',
                    "tamil_output.mp3"
                )
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
        
        else:  # English Only
            st.markdown("""
            <div class="language-box">
                <h3>🇬🇧 Simplified English</h3>
                <p>{}</p>
            </div>
            """.format(st.session_state.current_translation['english']), unsafe_allow_html=True)
            
            if voice_option:
                audio_file = generate_audio(
                    st.session_state.current_translation['english'],
                    'en',
                    "english_output.mp3"
                )
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')

# ==================== TAB 3: CHAT ASSISTANT ====================
with tab3:
    st.markdown("<div class='section-header'><h3>🤖 Ask Questions About Your Text</h3></div>", unsafe_allow_html=True)
    
    if not st.session_state.current_translation:
        st.warning("⚠️ Please first translate some text in Tab 2 to use the chat assistant.")
        st.info("The chatbot can answer questions about your translated text in both Tamil and English.")
    
    else:
        st.success("✅ Chatbot is ready! Ask questions about your translated text.")
        
        # Display current context
        with st.expander("📄 View Current Text Context"):
            col_orig, col_trans = st.columns(2)
            with col_orig:
                st.markdown("**Original:**")
                st.info(st.session_state.current_translation['original'][:200] + "...")
            with col_trans:
                if st.session_state.current_translation['tamil']:
                    st.markdown("**Tamil:**")
                    st.success(st.session_state.current_translation['tamil'][:200] + "...")
        
        # Chat interface
        st.markdown("---")
        st.markdown("### 💬 Chat with Assistant")
        
        # Chat input method
        chat_input_method = st.radio(
            "How to ask?",
            ["✍️ Type Question", "🎤 Speak Question"],
            horizontal=True,
            key="chat_input_method"
        )
        
        user_question = ""
        
        if chat_input_method == "✍️ Type Question":
            user_question = st.text_input(
                "Type your question in Tamil or English:",
                placeholder="E.g., 'What does this mean in Tamil?' or 'இதன் பொருள் என்ன?'"
            )
        else:
            # Voice input for chat
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if st.button("🎤 Speak Question", use_container_width=True):
                    st.info("Speaking... (Simulated - would use speech recognition)")
                    # In real implementation, this would capture voice
                    user_question = "What is the meaning of this text?"
            
            with col_v2:
                if st.button("🎧 Listen to Answer", use_container_width=True):
                    st.info("Would play answer audio")
        
        # Language for answer
        answer_language = st.radio(
            "Answer in:",
            ["🇮🇳 Tamil", "🇬🇧 English"],
            horizontal=True
        )
        
        ask_in_tamil = (answer_language == "🇮🇳 Tamil")
        
        # Ask button
        if user_question and st.button("🤖 Ask Question", type="primary"):
            # Get answer from chatbot
            answer = chatbot.answer_question(user_question, ask_in_tamil)
            
            # Add to chat history
            st.session_state.chat_history.append({
                'time': datetime.now().strftime("%H:%M"),
                'question': user_question,
                'answer': answer,
                'language': "Tamil" if ask_in_tamil else "English"
            })
            
            # Display answer
            st.markdown("---")
            st.markdown(f"**🤖 Assistant's Answer ({answer_language}):**")
            st.markdown(f"<div class='chat-message-bot'>{answer}</div>", unsafe_allow_html=True)
            
            # Generate voice for answer
            if st.button("🔊 Hear Answer Voice"):
                answer_audio = generate_audio(
                    answer,
                    'ta' if ask_in_tamil else 'en',
                    "chat_answer.mp3"
                )
                if answer_audio:
                    st.audio(answer_audio, format='audio/mp3')
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 📖 Chat History")
            
            for chat in reversed(st.session_state.chat_history[-5:]):
                st.markdown(f"**⏰ {chat['time']}** ({chat['language']})")
                st.markdown(f"<div class='chat-message-user'>🙂 **You:** {chat['question']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-message-bot'>🤖 **Assistant:** {chat['answer']}</div>", unsafe_allow_html=True)
                st.markdown("---")
        
        # Sample questions
        st.markdown("---")
        st.markdown("### 💡 Sample Questions")
        
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            if st.button("What is this text about?", use_container_width=True):
                st.session_state.sample_q = "What is this text about?"
        
        with col_q2:
            if st.button("Explain the Tamil translation", use_container_width=True):
                st.session_state.sample_q = "Explain the Tamil translation"
        
        col_q3, col_q4 = st.columns(2)
        
        with col_q3:
            if st.button("மொழிபெயர்ப்பு என்ன?", use_container_width=True):
                st.session_state.sample_q = "மொழிபெயர்ப்பு என்ன?"
        
        with col_q4:
            if st.button("எனக்கு விளக்கு", use_container_width=True):
                st.session_state.sample_q = "எனக்கு விளக்கு"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 📊 Dashboard")
    
    # Statistics
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("📚 Translations", len(st.session_state.translation_history))
    with col_stat2:
        st.metric("💬 Chats", len(st.session_state.chat_history))
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("## ⚡ Quick Actions")
    
    if st.button("🔄 Clear All", use_container_width=True):
        st.session_state.translation_history = []
        st.session_state.chat_history = []
        st.session_state.current_translation = None
        st.rerun()
    
    if st.button("📥 Export Chat", use_container_width=True):
        if st.session_state.chat_history:
            chat_text = "Talk2Tamil Chat History\n" + "="*50 + "\n"
            for chat in st.session_state.chat_history:
                chat_text += f"\n[{chat['time']}] {chat['language']}\n"
                chat_text += f"Q: {chat['question']}\n"
                chat_text += f"A: {chat['answer']}\n"
                chat_text += "-"*50 + "\n"
            
            st.download_button(
                "Download Chat History",
                chat_text,
                "talk2tamil_chat_history.txt",
                "text/plain"
            )
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("## 📅 Recent Activity")
    
    if st.session_state.translation_history:
        for item in reversed(st.session_state.translation_history[-3:]):
            st.markdown(f"⏰ **{item['time']}**")
            st.caption(f"📝 {item['input']}")
            st.caption(f"🎯 {item['output']}")
            st.markdown("---")
    else:
        st.info("No recent activity")
    
    st.markdown("---")
    
    # Help section
    st.markdown("## ❓ Help & Tips")
    st.markdown("""
    **Voice Input:**
    - Use Tab 1 for voice
    - Speak clearly
    - One sentence at a time
    
    **Chatbot:**
    - Ask about translations
    - Get explanations
    - Voice answers available
    
    **Translation:**
    - Any language supported
    - Download as PDF
    - Voice output
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <h4>🗣️🤖 Talk2Tamil: Complete Translation & Chat Assistant</h4>
    <p>🎤 Voice Input | 🌍 Multi-language | 🤖 AI Chat | 🔊 Voice Output | 📄 Documents</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit • Python • Google Translate • gTTS</p>
</div>
""", unsafe_allow_html=True)

# Add streamlit components for HTML
import streamlit.components.v1 as components
