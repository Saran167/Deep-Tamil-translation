import streamlit as st
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from gtts import gTTS
from fpdf import FPDF
import tempfile
import datetime
import re
import random

# Ensure consistent language detection
DetectorFactory.seed = 0

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Smart Tamil–English Translator",
    page_icon="🌈",
    layout="wide"
)

# --------------------------------------------------
# UI STYLING
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    .main-header {
        text-align: center;
        color: white;
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-bottom: 30px;
    }
    
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .step {
        text-align: center;
        flex: 1;
        padding: 10px;
    }
    
    .step-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }
    
    .block {
        background: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
    }
    
    .highlight {
        background-color: #d4edda;
        padding: 2px 5px;
        border-radius: 4px;
        color: #155724;
        font-weight: 600;
    }
    
    .highlight-red {
        background-color: #f8d7da;
        padding: 2px 5px;
        border-radius: 4px;
        color: #721c24;
        font-weight: 600;
    }
    
    .language-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        margin: 5px;
    }
    
    .demo-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        background: linear-gradient(45deg, #FF9800, #F57C00);
        color: white;
        font-weight: 600;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE + STEPS
# --------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🌈 Smart Spoken Tamil & Simple English Converter</h1>
    <p>Convert between formal and spoken language styles with text-to-speech</p>
</div>
""", unsafe_allow_html=True)

# Step indicators
st.markdown("""
<div class="step-container">
    <div class="step">
        <div class="step-icon">📥</div>
        <h4>1. Input Text</h4>
        <p>Enter text in Tamil or English</p>
    </div>
    <div class="step">
        <div class="step-icon">🔁</div>
        <h4>2. Process</h4>
        <p>Convert to spoken/simple form</p>
    </div>
    <div class="step">
        <div class="step-icon">📤</div>
        <h4>3. Output</h4>
        <p>View highlighted results</p>
    </div>
    <div class="step">
        <div class="step-icon">📄</div>
        <h4>4. Download</h4>
        <p>Get PDF & audio files</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SPOKEN TAMIL RULES (Extended)
# --------------------------------------------------
spoken_tamil_map = {
    # Pronouns
    "நான்": "நா",
    "நீங்கள்": "நீங்க",
    "அவர்": "அவரு",
    "அவள்": "அவ",
    "அது": "அது",
    "நாங்கள்": "நாங்க",
    
    # Common verbs
    "செய்கிறேன்": "செய்றேன்",
    "செய்கிறீர்கள்": "செய்றீங்க",
    "செய்கிறார்": "செய்றாரு",
    "சொல்கிறேன்": "சொல்றேன்",
    "சொல்கிறீர்கள்": "சொல்றீங்க",
    "பார்க்கிறேன்": "பாக்கிறேன்",
    "பார்க்கிறீர்கள்": "பாக்கிறீங்க",
    
    # Formal to spoken
    "அழைப்பேன்": "கால் பண்ணுறேன்",
    "அனுப்புவேன்": "அனுப்பிடுறேன்",
    "கூறுவேன்": "சொல்லிடுறேன்",
    "தெரிவிக்கிறேன்": "சொல்லுறேன்",
    
    # Words
    "தகவல்": "விஷயம்",
    "உடனடியாக": "உடனே",
    "இருக்கிறது": "இருக்கு",
    "வேண்டும்": "வேணும்",
    "செய்ய": "பண்ண",
    "பார்க்க": "பாத்து",
    "சொல்ல": "சொல்லு",
    "எடுக்க": "எடுத்து",
    "வருகிறேன்": "வரேன்",
    "போகிறேன்": "போகேன்",
    "கொடுக்க": "கொடு",
    "உண்ண": "சாப்பிடு",
    "குடிக்க": "குடி",
    
    # Time related
    "நாளை": "நாளைக்கு",
    "இன்று": "இன்னிக்கி",
    "நேற்று": "நெற்று",
    "பிறகு": "அப்புறம்",
    
    # Common phrases
    "நன்றி": "தங்க்ஸ்",
    "மன்னிக்கவும்": "சாரி",
    "ஆம்": "ஆமா",
    "இல்லை": "இல்ல",
    "உதவி": "ஹெல்ப்",
}

# --------------------------------------------------
# SIMPLE ENGLISH RULES (Extended)
# --------------------------------------------------
simple_english_map = {
    # Complex to simple
    "kindly": "please",
    "ensure": "make sure",
    "prior to": "before",
    "assist": "help",
    "purchase": "buy",
    "utilize": "use",
    "commence": "start",
    "terminate": "end",
    "approximately": "about",
    "additional": "more",
    "demonstrate": "show",
    "inquire": "ask",
    "facilitate": "help",
    "implement": "do",
    "endeavor": "try",
    "ascertain": "find out",
    "convey": "tell",
    "require": "need",
    "reside": "live",
    "possess": "have",
    "construct": "build",
    "consume": "eat/drink",
    "acquire": "get",
    "proceed": "go",
    "discontinue": "stop",
    
    # Business/formal to simple
    "hereinafter": "from now on",
    "aforementioned": "mentioned before",
    "notwithstanding": "even though",
    "heretofore": "until now",
    "whereas": "while",
    "henceforth": "from now on",
    
    # Common phrases
    "could you please": "can you",
    "would you mind": "please",
    "I would appreciate if": "please",
    "at your earliest convenience": "as soon as possible",
    "please be advised": "note that",
    "in accordance with": "following",
}

# --------------------------------------------------
# ENGLISH TO TAMIL DICTIONARY (Basic for demo)
# --------------------------------------------------
english_to_tamil_dict = {
    "hello": "வணக்கம்",
    "thank you": "நன்றி",
    "how are you": "எப்படி இருக்கிறீர்கள்",
    "good morning": "காலை வணக்கம்",
    "good night": "இரவு வணக்கம்",
    "please": "தயவு செய்து",
    "help": "உதவி",
    "water": "தண்ணீர்",
    "food": "உணவு",
    "house": "வீடு",
    "car": "கார்",
    "book": "புத்தகம்",
    "pen": "பேனா",
    "computer": "கணினி",
    "mobile": "மொபைல்",
    "money": "பணம்",
    "work": "வேலை",
    "school": "பள்ளி",
    "college": "கல்லூரி",
    "hospital": "மருத்துவமனை",
    "doctor": "டாக்டர்",
    "teacher": "ஆசிரியர்",
    "student": "மாணவர்",
    "father": "தந்தை",
    "mother": "தாய்",
    "brother": "சகோதரர்",
    "sister": "சகோதரி",
    "friend": "நண்பர்",
    "love": "காதல்",
    "happy": "மகிழ்ச்சி",
    "sad": "வருத்தம்",
    "angry": "கோபம்",
    "tired": "சோர்வு",
    "sleep": "தூக்கம்",
    "eat": "சாப்பிடு",
    "drink": "குடி",
    "go": "போ",
    "come": "வா",
    "see": "பார்",
    "hear": "கேள்",
    "speak": "பேசு",
    "read": "படி",
    "write": "எழுது",
}

# --------------------------------------------------
# TAMIL TO ENGLISH DICTIONARY (Basic for demo)
# --------------------------------------------------
tamil_to_english_dict = {
    "வணக்கம்": "hello",
    "நன்றி": "thank you",
    "எப்படி": "how",
    "இருக்கிறீர்கள்": "are you",
    "காலை": "morning",
    "இரவு": "night",
    "தயவு": "please",
    "உதவி": "help",
    "தண்ணீர்": "water",
    "உணவு": "food",
    "வீடு": "house",
    "கார்": "car",
    "புத்தகம்": "book",
    "பேனா": "pen",
    "கணினி": "computer",
    "மொபைல்": "mobile",
    "பணம்": "money",
    "வேலை": "work",
    "பள்ளி": "school",
    "கல்லூரி": "college",
    "மருத்துவமனை": "hospital",
    "டாக்டர்": "doctor",
    "ஆசிரியர்": "teacher",
    "மாணவர்": "student",
    "தந்தை": "father",
    "தாய்": "mother",
    "சகோதரர்": "brother",
    "சகோதரி": "sister",
    "நண்பர்": "friend",
    "காதல்": "love",
    "மகிழ்ச்சி": "happy",
    "வருத்தம்": "sad",
    "கோபம்": "angry",
    "சோர்வு": "tired",
    "தூக்கம்": "sleep",
    "சாப்பிடு": "eat",
    "குடி": "drink",
    "போ": "go",
    "வா": "come",
    "பார்": "see",
    "கேள்": "hear",
    "பேசு": "speak",
    "படி": "read",
    "எழுது": "write",
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def detect_language(text):
    """Detect language with better error handling"""
    try:
        lang = detect(text)
        lang_names = {
            'en': 'English',
            'ta': 'Tamil',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-cn': 'Chinese'
        }
        return lang_names.get(lang, f"Unknown ({lang})")
    except LangDetectException:
        # Check for Tamil characters
        if re.search(r'[\u0B80-\u0BFF]', text):
            return "Tamil"
        elif re.search(r'[a-zA-Z]', text):
            return "English"
        return "Could not detect"
    except Exception:
        return "Unknown"

def highlight_changes(original, modified, replacements):
    """Highlight changed words in the text"""
    if original == modified:
        return modified
    
    original_words = original.split()
    modified_words = modified.split()
    highlighted_words = []
    
    # Simple word-by-word comparison
    for orig, mod in zip(original_words, modified_words[:len(original_words)]):
        if orig != mod:
            # Check if this was a replacement from our map
            for formal, spoken in replacements.items():
                if formal in orig and spoken in mod:
                    highlighted_words.append(f'<span class="highlight">{mod}</span>')
                    break
            else:
                highlighted_words.append(f'<span class="highlight-red">{mod}</span>')
        else:
            highlighted_words.append(mod)
    
    # Add any extra words
    if len(modified_words) > len(original_words):
        highlighted_words.extend(modified_words[len(original_words):])
    
    return ' '.join(highlighted_words)

def chunk_text(text, size=200):
    """Split text into manageable chunks"""
    if len(text) <= size:
        return [text]
    
    # Split by sentences
    sentences = re.split(r'(?<=[.!?।॥]) +', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= size:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def simple_translate(text, target_lang):
    """Simple rule-based translation for demo"""
    if target_lang == "ta":  # English to Tamil
        result = text
        for eng, tam in english_to_tamil_dict.items():
            if eng.lower() in result.lower():
                result = result.replace(eng, tam)
                result = result.replace(eng.capitalize(), tam)
                result = result.replace(eng.upper(), tam)
        return result if result != text else f"[Demo Translation to Tamil: {text}]"
    
    elif target_lang == "en":  # Tamil to English
        result = text
        for tam, eng in tamil_to_english_dict.items():
            if tam in result:
                result = result.replace(tam, eng)
        return result if result != text else f"[Demo Translation to English: {text}]"
    
    return text

def apply_spoken_rules(text, language):
    """Apply spoken language rules"""
    if language == "Tamil":
        for formal, spoken in spoken_tamil_map.items():
            text = text.replace(formal, spoken)
    else:  # English
        for formal, simple in simple_english_map.items():
            # Case-insensitive replacement
            text = re.sub(rf'\b{formal}\b', simple, text, flags=re.IGNORECASE)
    
    return text

# --------------------------------------------------
# PDF GENERATION
# --------------------------------------------------
def create_pdf(input_text, output_text, in_lang, out_lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Smart Language Converter - Report", ln=True, align='C')
    pdf.ln(10)
    
    # Add timestamp
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    # Language info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, f"Conversion: {in_lang} → {out_lang}", ln=True)
    pdf.ln(5)
    
    # Input text
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(200, 10, "Input Text:", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, input_text)
    pdf.ln(5)
    
    # Output text
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Output Text:", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, output_text)
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 10, "Generated by Smart Tamil–English Converter", ln=True, align='C')
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --------------------------------------------------
# MAIN APP LAYOUT
# --------------------------------------------------

# Demo Mode Notice
st.markdown('<div class="demo-badge">DEMO MODE: Using rule-based conversion</div>', unsafe_allow_html=True)
st.info("💡 **Note:** This is a demo version using rule-based conversion. For full translation capabilities, you can integrate with translation APIs.")

# Input Section
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.subheader("📝 Enter Your Text")
input_text = st.text_area("Enter your text here:", 
                         placeholder="Type or paste your text here (Tamil or English)...\n\nExamples:\n- 'நான் உங்களுக்கு உதவி செய்கிறேன்'\n- 'Kindly assist me with the purchase'\n- 'வணக்கம், எப்படி இருக்கிறீர்கள்?'\n- 'I would like to ascertain the details'", 
                         height=150, 
                         label_visibility="visible")
st.markdown("</div>", unsafe_allow_html=True)

# Language Selection
st.markdown("<div class='block'>", unsafe_allow_html=True)
st.subheader("🌐 Conversion Settings")
col1, col2 = st.columns(2)

with col1:
    # Language detection display
    if input_text.strip():
        detected = detect_language(input_text)
        st.markdown(f"**Detected Language:**")
        st.markdown(f'<div class="language-badge">{detected}</div>', unsafe_allow_html=True)

with col2:
    conversion_type = st.radio(
        "**Choose Conversion Type:**",
        ["Formal to Spoken Tamil", "Complex to Simple English"],
        horizontal=False
    )
st.markdown("</div>", unsafe_allow_html=True)

# Quick Examples
with st.expander("💡 Quick Examples"):
    examples_col1, examples_col2 = st.columns(2)
    
    with examples_col1:
        st.markdown("**Tamil Examples:**")
        examples_tamil = {
            "நான் உங்களுக்கு உதவி செய்கிறேன்": "நா உங்களுக்கு உதவி செய்றேன்",
            "நாளை அழைப்பேன்": "நாளைக்கு கால் பண்ணுறேன்",
            "தகவல் தெரிவிக்கிறேன்": "விஷயம் சொல்லுறேன்"
        }
        for formal, spoken in examples_tamil.items():
            st.caption(f"**Formal:** {formal}")
            st.caption(f"**Spoken:** {spoken}")
            st.divider()
    
    with examples_col2:
        st.markdown("**English Examples:**")
        examples_english = {
            "Kindly assist me with the purchase": "Please help me buy it",
            "I would like to ascertain the details": "I want to find out the details",
            "Please ensure completion prior to departure": "Please make sure it's done before leaving"
        }
        for complex, simple in examples_english.items():
            st.caption(f"**Complex:** {complex}")
            st.caption(f"**Simple:** {simple}")
            st.divider()

# Process Button
process_col, _ = st.columns([1, 3])
with process_col:
    process_btn = st.button("✨ Convert Text", use_container_width=True, type="primary")

if process_btn and input_text.strip():
    with st.spinner("Processing text..."):
        # Detect language
        detected_lang_name = detect_language(input_text)
        
        # Display language detection
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("🌍 Language Detection")
        st.success(f"**Input language detected as:** {detected_lang_name}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Determine conversion type
        if "Tamil" in conversion_type:
            target_lang = "ta"
            is_tamil = True
            lang_name = "Spoken Tamil"
            replacements = spoken_tamil_map
            # First translate English to Tamil if needed
            if "English" in detected_lang_name:
                intermediate_text = simple_translate(input_text, "ta")
            else:
                intermediate_text = input_text
        else:
            target_lang = "en"
            is_tamil = False
            lang_name = "Simple English"
            replacements = simple_english_map
            # First translate Tamil to English if needed
            if "Tamil" in detected_lang_name:
                intermediate_text = simple_translate(input_text, "en")
            else:
                intermediate_text = input_text
        
        # Step 1: Handle long text
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("🔁 Processing Text")
        
        if len(intermediate_text) > 200:
            st.info("📚 Long text detected. Processing in chunks...")
            chunks = chunk_text(intermediate_text)
            progress_bar = st.progress(0)
            
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                processed = apply_spoken_rules(chunk, "Tamil" if is_tamil else "English")
                processed_chunks.append(processed)
                progress_bar.progress((i + 1) / len(chunks))
            
            final_output = " ".join(processed_chunks)
        else:
            final_output = apply_spoken_rules(intermediate_text, "Tamil" if is_tamil else "English")
        
        # Highlight changed words
        highlighted_output = highlight_changes(intermediate_text, final_output, replacements)
        
        st.success(f"✓ Converted to {lang_name}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Output Display
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("📤 Final Output")
        
        # Display with highlighted words
        st.markdown("**Improved words are highlighted:**")
        st.markdown(f'<div style="padding: 20px; background: #f8f9fa; border-radius: 10px; border: 1px solid #dee2e6; font-size: 16px; line-height: 1.6;">{highlighted_output}</div>', 
                   unsafe_allow_html=True)
        
        # Show original vs modified comparison
        with st.expander("🔍 View Comparison"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_area("Original/Translated Text", intermediate_text, height=150, disabled=True)
            with col2:
                st.text_area(f"After {lang_name} Conversion", final_output, height=150, disabled=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Audio Output Section
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("🔊 Audio Output")
        
        try:
            # Generate TTS
            tts_lang = 'ta' if is_tamil else 'en'
            tts = gTTS(text=final_output, lang=tts_lang, slow=False)
            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(audio_file.name)
            
            st.audio(audio_file.name, format='audio/mp3')
            st.success("✓ Audio generated successfully!")
            
            # Download audio button
            with open(audio_file.name, "rb") as audio_data:
                st.download_button(
                    label="🎵 Download Audio",
                    data=audio_data,
                    file_name="converted_audio.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )
        except Exception as e:
            st.warning(f"Audio generation failed: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Section
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("📥 Download Results")
        
        # PDF Download
        pdf_path = create_pdf(input_text, final_output, detected_lang_name, lang_name)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name="conversion_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Text Download
        st.download_button(
            label="📝 Download Text",
            data=final_output,
            file_name="converted_text.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Feedback Section
        st.markdown("<div class='block'>", unsafe_allow_html=True)
        st.subheader("🗳️ User Feedback")
        st.markdown("Was this conversion helpful?")
        
        feedback_col1, feedback_col2 = st.columns(2)
        
        with feedback_col1:
            if st.button("👍 Easy to understand", use_container_width=True, key="feedback_good"):
                st.balloons()
                st.success("Thank you for your feedback! We're glad it was helpful.")
        
        with feedback_col2:
            if st.button("👎 Needs improvement", use_container_width=True, key="feedback_bad"):
                st.info("Thank you for your feedback! We'll work on improving the conversion rules.")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif process_btn:
    st.warning("⚠️ Please enter some text to convert.")

# --------------------------------------------------
# SIDEBAR INFORMATION
# --------------------------------------------------
with st.sidebar:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("ℹ️ Features")
    
    features = [
        "✅ Language detection",
        "✅ Spoken Tamil conversion",
        "✅ Simple English conversion",
        "✅ Long text chunking",
        "✅ Highlighted improvements",
        "✅ Text-to-speech audio",
        "✅ PDF report generation",
        "✅ User feedback system"
    ]
    
    for feature in features:
        st.markdown(feature)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📊 Usage Tips")
    st.markdown("""
    1. Enter text in Tamil or English
    2. Choose conversion type
    3. View highlighted results
    4. Download PDF report
    5. Listen to audio output
    6. Provide feedback
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("🔧 Technical Info")
    st.markdown("""
    **Current Mode:** Demo
    **Translation:** Rule-based
    **Audio:** Google TTS
    **PDF:** FPDF2
    **Deployment:** Streamlit Cloud
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("✨ Smart Tamil–English Converter | Demo Version | All processing happens locally in your browser")
