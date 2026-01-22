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
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .language-box {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .simplified-box {
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
    }
    .output-box {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .highlight {
        background-color: #FFFBEB;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #F59E0B;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCTIONS ====================

def simplify_english(text):
    """
    Comprehensive English simplifier for Indian users
    """
    # Expanded simplification dictionary
    simplification_dict = {
        # Technical/Academic terms
        'artificial intelligence': 'smart computer systems',
        'machine learning': 'computers that learn from data',
        'algorithms': 'step-by-step instructions',
        'computer science': 'computer studies',
        'software': 'computer programs',
        'programmed': 'given instructions',
        'data': 'information',
        'systems': 'setups or arrangements',
        'performance': 'work quality',
        'applications': 'uses or programs',
        'robotics': 'robot technology',
        'predictions': 'guesses about future',
        'recognition': 'identifying things',
        'understanding': 'knowing',
        
        # Complex verbs
        'focuses on': 'works on',
        'creates': 'makes',
        'designed to': 'made to',
        'perform tasks': 'do jobs',
        'utilizes': 'uses',
        'improves': 'gets better',
        'makes decisions': 'chooses',
        
        # Complex adjectives
        'useful': 'helpful',
        'efficient': 'works well',
        'effective': 'works good',
        'complex': 'complicated',
        'sophisticated': 'advanced',
        
        # Phrases
        'branch of': 'part of',
        'such as': 'like',
        'instead of': 'rather than',
        'over time': 'with time',
        'by using': 'using',
        'every single': 'each',
        
        # Academic phrases
        'in many fields': 'in many areas',
        'everyday applications': 'daily uses',
        'voice assistants': 'voice helpers',
        'recommendation systems': 'suggestion tools',
    }
    
    # Convert to lowercase for processing
    lower_text = text.lower()
    
    # Replace longer phrases first
    for complex_phrase, simple_phrase in simplification_dict.items():
        if complex_phrase in lower_text:
            # Case-insensitive replacement
            import re
            text = re.compile(re.escape(complex_phrase), re.IGNORECASE).sub(simple_phrase, text)
    
    # Additional simplifications
    simplifications = [
        # Remove markdown/formatting
        ('**', ''),
        ('*', ''),
        ('#', ''),
        
        # Simplify punctuation
        ('(', ' ('),
        (')', ') '),
        (';', '.'),
        
        # Break long sentences
        (', which', '. This'),
        (', and', '. And'),
        (', but', '. But'),
    ]
    
    for old, new in simplifications:
        text = text.replace(old, new)
    
    # Split into sentences and simplify each
    sentences = text.split('. ')
    simplified_sentences = []
    
    for sentence in sentences:
        if sentence.strip():
            # Make sentences shorter
            words = sentence.split()
            if len(words) > 20:
                # Split very long sentences
                mid = len(words) // 2
                part1 = ' '.join(words[:mid])
                part2 = ' '.join(words[mid:])
                simplified_sentences.append(part1 + '.')
                simplified_sentences.append(part2)
            else:
                simplified_sentences.append(sentence)
    
    result = '. '.join(simplified_sentences)
    
    # Ensure proper spacing
    result = ' '.join(result.split())
    
    # Capitalize first letter
    if result:
        result = result[0].upper() + result[1:]
    
    return result

def translate_to_tamil(text):
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        translation = translator.translate(text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def generate_tamil_audio(text, filename="tamil_audio.mp3"):
    """
    Generate Tamil audio with multiple fallback methods
    """
    try:
        # Method 1: Direct gTTS
        tts = gTTS(text=text, lang='ta', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.warning(f"Tamil TTS method 1 failed. Trying alternative...")
        
        try:
            # Method 2: Google Translate TTS API
            text_encoded = urllib.parse.quote(text)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text_encoded}&tl=ta&client=tw-ob"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
            else:
                st.error(f"TTS API failed: {response.status_code}")
                return None
                
        except Exception as e2:
            st.error(f"All Tamil TTS methods failed")
            return None

def generate_english_audio(text, filename="english_audio.mp3"):
    """
    Generate English audio with fallback
    """
    try:
        # Method 1: gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.warning(f"English TTS method 1 failed. Trying alternative...")
        
        try:
            # Method 2: PyTTSx3 if installed
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            engine.save_to_file(text, filename)
            engine.runAndWait()
            
            return filename
            
        except:
            # Method 3: Use online service
            try:
                text_encoded = urllib.parse.quote(text)
                url = f"http://api.voicerss.org/?key=demo&hl=en-us&src={text_encoded}"
                
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    return filename
            except:
                return None
        return None

def create_pdf(content, filename, language):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Add title
    c.drawString(100, 750, f"Talk2Tamil - {language} Translation")
    c.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add content
    y = 700
    lines = content.split('\n')
    
    for line in lines:
        words = line.split()
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            
            if c.stringWidth(test_line, "Helvetica", 12) > 400:
                # Write line and start new
                c.drawString(100, y, ' '.join(current_line[:-1]))
                y -= 20
                current_line = [word]
                
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
        
        if current_line:
            c.drawString(100, y, ' '.join(current_line))
            y -= 20
    
    c.save()

# ==================== MAIN APP ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>🗣️ Talk2Tamil: Smart Translator</h1>
    <p>🌍 Any Language → 🇮🇳 Tamil OR 🇬🇧 Simple English | 🔊 Voice | 📄 PDF</p>
</div>
""", unsafe_allow_html=True)

# Initialize session
if 'history' not in st.session_state:
    st.session_state.history = []

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Text")
    
    input_method = st.radio(
        "✨ Choose input method:",
        ["✍️ Type/Paste Text", "📁 Upload File"]
    )
    
    input_text = ""
    
    if input_method == "✍️ Type/Paste Text":
        input_text = st.text_area(
            "Type or paste text here:",
            height=200,
            value="Artificial Intelligence (AI) is a branch of computer science that focuses on creating machines or software that can think, learn, and make decisions like humans. AI systems are designed to perform tasks such as understanding language, recognizing images, solving problems, and making predictions by using data and algorithms. Instead of being programmed for every single action, AI can learn from experience and improve its performance over time, which makes it useful in many fields like education, healthcare, banking, robotics, and everyday applications such as voice assistants and recommendation systems.",
            help="You can type in any language"
        )
    
    elif input_method == "📁 Upload File":
        uploaded_file = st.file_uploader("Choose a file", type=['txt', 'docx', 'pdf'])
        if uploaded_file:
            if uploaded_file.name.endswith('.txt'):
                input_text = uploaded_file.read().decode()
            st.text_area("Extracted Text", input_text, height=150)

with col2:
    st.markdown("### ⚙️ Output Settings")
    
    output_option = st.radio(
        "🎯 Select output:",
        ["🇮🇳 Tamil Only", "🇬🇧 Simple English Only", "🌍 Both"]
    )
    
    st.markdown("---")
    
    voice_option = st.checkbox("🔊 Add voice output", value=True)
    doc_option = st.checkbox("📄 Generate downloadable file", value=True)
    
    st.markdown("---")
    
    process_btn = st.button(
        "✨ TRANSLATE & SIMPLIFY",
        type="primary",
        use_container_width=True
    )

# Process
if process_btn and input_text.strip():
    with st.spinner("🔄 Processing..."):
        # Store original
        original = input_text
        
        # Get outputs
        tamil_output = ""
        english_output = ""
        
        if output_option in ["🇮🇳 Tamil Only", "🌍 Both"]:
            tamil_output = translate_to_tamil(original)
        
        if output_option in ["🇬🇧 Simple English Only", "🌍 Both"]:
            english_output = simplify_english(original)
            
            # Show what changed
            if english_output != original:
                st.markdown("### 🔄 Simplification Changes")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Original:**")
                    st.info(original[:200] + "...")
                with col_b:
                    st.markdown("**Simplified:**")
                    st.success(english_output[:200] + "...")
        
        # Store in session
        st.session_state.current = {
            'tamil': tamil_output,
            'english': english_output,
            'original': original
        }
        
        # Add to history
        st.session_state.history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'output': output_option,
            'text': original[:50] + "..."
        })

# Display Results
if 'current' in st.session_state and st.session_state.current:
    st.markdown("---")
    st.markdown("## 📊 Results")
    
    if output_option == "🌍 Both":
        col_t, col_e = st.columns(2)
        
        with col_t:
            st.markdown("""
            <div class="language-box">
                <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(st.session_state.current['tamil'])
            
            if voice_option and st.session_state.current['tamil']:
                audio = generate_tamil_audio(st.session_state.current['tamil'])
                if audio:
                    st.audio(audio, format='audio/mp3')
                    st.success("✅ Tamil voice generated")
        
        with col_e:
            st.markdown("""
            <div class="language-box simplified-box">
                <h3>🇬🇧 Simple English</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(st.session_state.current['english'])
            
            if voice_option and st.session_state.current['english']:
                audio = generate_english_audio(st.session_state.current['english'])
                if audio:
                    st.audio(audio, format='audio/mp3')
                    st.success("✅ English voice generated")
    
    elif output_option == "🇮🇳 Tamil Only":
        st.markdown("""
        <div class="language-box">
            <h3>🇮🇳 தமிழ் மொழிபெயர்ப்பு</h3>
            <p>{}</p>
        </div>
        """.format(st.session_state.current['tamil']), unsafe_allow_html=True)
        
        if voice_option and st.session_state.current['tamil']:
            audio = generate_tamil_audio(st.session_state.current['tamil'])
            if audio:
                st.audio(audio, format='audio/mp3')
    
    else:  # Simple English Only
        st.markdown("""
        <div class="language-box simplified-box">
            <h3>🇬🇧 Simple English (Easy to Understand)</h3>
            <p>{}</p>
        </div>
        """.format(st.session_state.current['english']), unsafe_allow_html=True)
        
        if voice_option and st.session_state.current['english']:
            audio = generate_english_audio(st.session_state.current['english'])
            if audio:
                st.audio(audio, format='audio/mp3')
    
    # Download options
    if doc_option:
        st.markdown("---")
        st.markdown("### 📥 Download Options")
        
        if output_option in ["🇮🇳 Tamil Only", "🌍 Both"] and st.session_state.current['tamil']:
            if st.button("📄 Download Tamil as PDF"):
                create_pdf(st.session_state.current['tamil'], "tamil_translation.pdf", "Tamil")
                with open("tamil_translation.pdf", "rb") as f:
                    st.download_button(
                        "⬇️ Click to Download Tamil PDF",
                        f.read(),
                        "tamil_translation.pdf",
                        "application/pdf"
                    )
        
        if output_option in ["🇬🇧 Simple English Only", "🌍 Both"] and st.session_state.current['english']:
            if st.button("📄 Download English as PDF"):
                create_pdf(st.session_state.current['english'], "english_translation.pdf", "Simple English")
                with open("english_translation.pdf", "rb") as f:
                    st.download_button(
                        "⬇️ Click to Download English PDF",
                        f.read(),
                        "english_translation.pdf",
                        "application/pdf"
                    )

# Sidebar
with st.sidebar:
    st.markdown("## 📖 History")
    
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"⏰ **{item['time']}** - {item['output']}")
            st.caption(f"📝 {item['text']}")
    else:
        st.info("No translations yet")
    
    st.markdown("---")
    
    st.markdown("## 💡 Quick Tips")
    st.markdown("""
    - **Simple English** makes complex text easy
    - **Voice output** helps non-readers
    - **Download PDF** for offline use
    - Works with **any language**
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Clear History"):
        st.session_state.history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 <strong>Talk2Tamil</strong> - Smart Translation for Everyone</p>
    <p>🌍 Any Language → 🇮🇳 Tamil | 🇬🇧 Simple English | 🔊 Voice | 📄 PDF</p>
</div>
""", unsafe_allow_html=True)
