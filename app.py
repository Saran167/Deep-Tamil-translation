import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import base64
from datetime import datetime
import os
import requests
import urllib.parse
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
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_translation' not in st.session_state:
    st.session_state.current_translation = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'voice_input_text' not in st.session_state:
    st.session_state.voice_input_text = ""
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

# ==================== FUNCTIONS ====================

def translate_to_tamil(text):
    """Translate text to Tamil"""
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        return translator.translate(text)
    except:
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
    }
    
    # Simple word replacement
    simplified_text = text
    for complex_word, simple_word in simplification_dict.items():
        if complex_word in simplified_text.lower():
            import re
            simplified_text = re.compile(re.escape(complex_word), re.IGNORECASE).sub(simple_word, simplified_text)
    
    return simplified_text

def generate_audio(text, language='ta', filename="audio.mp3"):
    """Generate audio from text"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

# ==================== CHATBOT CLASS ====================
class SimpleChatbot:
    def __init__(self):
        self.context = ""
    
    def set_context(self, original_text, tamil_translation, english_translation):
        self.context = f"Original: {original_text}\nTamil: {tamil_translation}\nEnglish: {english_translation}"
    
    def answer_question(self, question, ask_in_tamil=False):
        if "meaning" in question.lower() or "explain" in question.lower():
            if ask_in_tamil:
                return "இது உங்கள் உரையின் மொழிபெயர்ப்பு ஆகும்."
            else:
                return "This is a translation of your text."
        elif "tamil" in question.lower():
            if ask_in_tamil:
                return "இது தமிழ் மொழிபெயர்ப்பு."
            else:
                return "This is the Tamil translation."
        elif "english" in question.lower():
            if ask_in_tamil:
                return "இது எளிய ஆங்கிலம்."
            else:
                return "This is simplified English."
        else:
            if ask_in_tamil:
                return "மன்னிக்கவும், இந்த கேள்விக்கு பதில் தெரியவில்லை."
            else:
                return "I'm sorry, I don't know the answer."

chatbot = SimpleChatbot()

# ==================== MAIN APP ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>🗣️🤖 Talk2Tamil: Voice & Chat Assistant</h1>
    <p>🎤 Voice Input | 🌍 Translation | 🤖 Q&A Chatbot | 🔊 Voice Output | 📄 Documents</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🎤 Voice Input", "📝 Text/Image Input", "🤖 Chat Assistant"])

# ==================== TAB 1: VOICE INPUT ====================
with tab1:
    st.markdown("<div class='section-header'><h3>🎤 Speak in Tamil or English</h3></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='voice-box'>
            <h4>🎙️ Voice Input Instructions</h4>
            <p>1. Type text in the box below<br>
            2. Click translate to process<br>
            3. Get voice output</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice input simulation (text input)
        voice_input = st.text_area(
            "🎤 Type what you want to say:",
            height=150,
            placeholder="Type your message here as if you were speaking...",
            value=st.session_state.voice_input_text,
            key="voice_input_area"
        )
        
        # Update session state
        if voice_input:
            st.session_state.voice_input_text = voice_input
        
        # Translate button
        if st.button("✨ Translate Voice Input", type="primary", key="translate_voice"):
            if st.session_state.voice_input_text:
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
        - Type clearly
        - Use simple sentences
        
        **English:**
        - Clear sentences
        - Avoid jargon
        """)

# ==================== TAB 2: TEXT/IMAGE INPUT ====================
with tab2:
    st.markdown("<div class='section-header'><h3>📝 Type, Paste, or Upload</h3></div>", unsafe_allow_html=True)
    
    col_input, col_settings = st.columns([2, 1])
    
    with col_input:
        # Input method
        input_method = st.radio(
            "✨ Choose input method:",
            ["✍️ Type/Paste Text", "📁 Upload File (Coming Soon)"],
            key="input_method"
        )
        
        # Initialize input_text variable
        input_text = ""
        
        if input_method == "✍️ Type/Paste Text":
            input_text = st.text_area(
                "Enter text in any language:",
                height=200,
                placeholder="Type or paste your text here...\nExample: 'Your bank account needs verification.'",
                key="text_input_main"
            )
        else:
            st.info("📁 File upload feature coming soon!")
            # For now, allow text input
            input_text = st.text_area(
                "Or type text here:",
                height=150,
                key="alt_text_input"
            )
    
    with col_settings:
        st.markdown("### ⚙️ Output Settings")
        
        output_option = st.radio(
            "🎯 Select output:",
            ["🇮🇳 Tamil Only", "🇬🇧 Simple English Only", "🌍 Both Languages"],
            key="output_option"
        )
        
        st.markdown("---")
        
        voice_option = st.checkbox("🔊 Generate voice output", value=True, key="voice_option")
        
        st.markdown("---")
        
        # Process button
        process_btn = st.button(
            "✨ TRANSLATE NOW",
            type="primary",
            use_container_width=True,
            key="translate_btn_main"
        )
    
    # Process translation
    if process_btn:
        # Check which input_text to use
        if input_method == "✍️ Type/Paste Text":
            text_to_translate = st.session_state.text_input_main
        else:
            text_to_translate = st.session_state.alt_text_input if 'alt_text_input' in st.session_state else ""
        
        if text_to_translate and text_to_translate.strip():
            with st.spinner("🔄 Processing translation..."):
                tamil_translation = ""
                english_translation = ""
                
                if output_option in ["🇮🇳 Tamil Only", "🌍 Both Languages"]:
                    tamil_translation = translate_to_tamil(text_to_translate)
                
                if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
                    english_translation = simplify_english(text_to_translate)
                
                # Store in session
                st.session_state.current_translation = {
                    'original': text_to_translate,
                    'tamil': tamil_translation,
                    'english': english_translation
                }
                
                # Set chatbot context
                chatbot.set_context(text_to_translate, tamil_translation, english_translation)
                
                # Add to history
                st.session_state.translation_history.append({
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'input': text_to_translate[:50] + "..." if len(text_to_translate) > 50 else text_to_translate,
                    'output': output_option
                })
        else:
            st.warning("⚠️ Please enter some text to translate.")

# Display translation results if available
if st.session_state.current_translation:
    st.markdown("---")
    st.markdown("## 📊 Translation Results")
    
    # Show what changed if English was simplified
    if output_option in ["🇬🇧 Simple English Only", "🌍 Both Languages"]:
        original = st.session_state.current_translation['original']
        english = st.session_state.current_translation['english']
        if english != original:
            st.markdown("### 🔄 Simplification Changes")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Original:**")
                st.info(original[:200] + "..." if len(original) > 200 else original)
            with col_b:
                st.markdown("**Simplified:**")
                st.success(english[:200] + "..." if len(english) > 200 else english)
    
    if output_option == "🌍 Both Languages":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("""
            <div class="language-box">
                <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(st.session_state.current_translation['tamil'])
            
            if voice_option and st.session_state.current_translation['tamil']:
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
        
        if voice_option and st.session_state.current_translation['tamil']:
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
        
        # Chat interface
        st.markdown("### 💬 Chat with Assistant")
        
        # Question input
        user_question = st.text_input(
            "Type your question in Tamil or English:",
            placeholder="E.g., 'What does this mean in Tamil?' or 'இதன் பொருள் என்ன?'",
            key="question_input"
        )
        
        # Language for answer
        answer_language = st.radio(
            "Answer in:",
            ["🇮🇳 Tamil", "🇬🇧 English"],
            horizontal=True,
            key="answer_lang"
        )
        
        ask_in_tamil = (answer_language == "🇮🇳 Tamil")
        
        # Ask button
        if user_question and st.button("🤖 Ask Question", type="primary", key="ask_btn"):
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
            st.markdown(f"**🤖 Assistant's Answer ({answer_language}):**")
            st.markdown(f"<div class='chat-message-bot'>{answer}</div>", unsafe_allow_html=True)
            
            # Generate voice for answer
            if st.button("🔊 Hear Answer Voice", key="hear_answer"):
                answer_audio = generate_audio(
                    answer,
                    'ta' if ask_in_tamil else 'en',
                    "chat_answer.mp3"
                )
                if answer_audio:
                    st.audio(answer_audio, format='audio/mp3')
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 📖 Chat History")
            
            for chat in reversed(st.session_state.chat_history[-5:]):
                st.markdown(f"**⏰ {chat['time']}** ({chat['language']})")
                st.markdown(f"<div class='chat-message-user'>🙂 **You:** {chat['question']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-message-bot'>🤖 **Assistant:** {chat['answer']}</div>", unsafe_allow_html=True)
                st.markdown("---")

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
    if st.button("🔄 Clear All", use_container_width=True, key="clear_all"):
        st.session_state.translation_history = []
        st.session_state.chat_history = []
        st.session_state.current_translation = None
        st.session_state.voice_input_text = ""
        st.rerun()

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <h4>🗣️🤖 Talk2Tamil: Complete Translation & Chat Assistant</h4>
    <p>🎤 Voice Input | 🌍 Multi-language | 🤖 AI Chat | 🔊 Voice Output | 📄 Documents</p>
</div>
""", unsafe_allow_html=True)
