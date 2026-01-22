import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
import io
import base64
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Talk2Tamil - Multilingual Assistant",
    page_icon="🗣️",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
    }
    .language-box {
        background-color: #F0F9FF;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
    .output-box {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #F59E0B;
        margin: 1rem 0;
    }
    .voice-button {
        background-color: #10B981;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .download-btn {
        background-color: #8B5CF6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("<h1 class='main-header'>🗣️ Talk2Tamil: Multilingual Assistant</h1>", unsafe_allow_html=True)
st.markdown("**Translate any text to Tamil OR Simple English with voice output**")

# Initialize session state
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []
if 'current_output' not in st.session_state:
    st.session_state.current_output = None

# Function to translate to Tamil
def translate_to_tamil(text):
    try:
        translator = GoogleTranslator(source='auto', target='ta')
        translation = translator.translate(text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails

# Function to simplify English text
def simplify_english(text):
    """
    Simple rule-based English simplifier
    Replace complex words with simpler ones
    """
    simplification_dict = {
        # Legal terms
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
        'verify': 'check',
        'submit': 'give',
        'application': 'form',
        'documentation': 'papers',
        'financial': 'money',
        'portfolio': 'collection',
        'diversification': 'spreading',
        'mitigate': 'reduce',
        'volatility': 'changes',
        
        # Banking terms
        'transaction': 'money transfer',
        'authentication': 'verification',
        'credentials': 'login details',
        'suspended': 'stopped',
        'unauthorized': 'not allowed',
        'fraudulent': 'fake',
        'notification': 'alert',
        
        # Government terms
        'implementation': 'putting in place',
        'regulation': 'rule',
        'compliance': 'following rules',
        'authorization': 'permission',
        'certificate': 'proof paper',
    }
    
    # Convert to lowercase for matching
    simplified_text = text
    for complex_word, simple_word in simplification_dict.items():
        # Replace whole words only (case insensitive)
        simplified_text = ' '.join([
            simple_word if word.lower() == complex_word.lower() else word 
            for word in simplified_text.split()
        ])
    
    # Shorten long sentences
    sentences = simplified_text.split('. ')
    short_sentences = []
    for sentence in sentences:
        if len(sentence.split()) > 20:
            # Split into two sentences
            words = sentence.split()
            half = len(words) // 2
            short_sentences.append(' '.join(words[:half]) + '.')
            short_sentences.append(' '.join(words[half:]))
        else:
            short_sentences.append(sentence)
    
    return '. '.join(short_sentences)

# Function to generate Tamil audio
def generate_tamil_audio(text, filename="tamil_audio.mp3"):
    try:
        tts = gTTS(text=text, lang='ta', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Audio generation error: {str(e)}")
        return None

# Function to generate English audio
def generate_english_audio(text, filename="english_audio.mp3"):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"Audio generation error: {str(e)}")
        return None

# Function to create download link
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Your Text")
    
    # Input method selection
    input_method = st.radio(
        "How would you like to input text?",
        ["Type/Paste Text", "Upload File", "Record Voice (Coming Soon)"]
    )
    
    input_text = ""
    
    if input_method == "Type/Paste Text":
        input_text = st.text_area(
            "Enter text in any language:",
            height=150,
            placeholder="Type or paste your text here. Example: 'Your bank account requires immediate verification.'"
        )
    
    elif input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload a text file", type=['txt', 'docx', 'pdf'])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.txt'):
                input_text = uploaded_file.read().decode()
            elif uploaded_file.name.endswith('.docx'):
                # For DOCX files
                import docx
                doc = docx.Document(uploaded_file)
                input_text = "\n".join([para.text for para in doc.paragraphs])
            elif uploaded_file.name.endswith('.pdf'):
                # For PDF files
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                input_text = ""
                for page in pdf_reader.pages:
                    input_text += page.extract_text()
            st.text_area("Extracted Text", input_text, height=150)

with col2:
    st.markdown("### ⚙️ Output Settings")
    
    # Output language selection
    output_option = st.radio(
        "Choose output format:",
        ["Tamil Only", "Simple English Only", "Both Tamil & English"]
    )
    
    # Voice output option
    voice_option = st.checkbox("🔊 Generate voice output", value=True)
    
    # Document download option
    doc_option = st.checkbox("📄 Generate downloadable document", value=True)
    
    # Process button
    process_btn = st.button("🚀 Translate & Simplify", type="primary", use_container_width=True)

# Process when button is clicked
if process_btn and input_text.strip():
    with st.spinner("Processing your request..."):
        # Store original text
        st.session_state.original_text = input_text
        
        # Get translations
        tamil_translation = ""
        simple_english = ""
        
        if output_option in ["Tamil Only", "Both Tamil & English"]:
            tamil_translation = translate_to_tamil(input_text)
        
        if output_option in ["Simple English Only", "Both Tamil & English"]:
            # First translate to English if not already in English
            if not input_text.isascii():  # Simple check if text is non-English
                english_version = GoogleTranslator(source='auto', target='en').translate(input_text)
                simple_english = simplify_english(english_version)
            else:
                simple_english = simplify_english(input_text)
        
        # Store in session
        st.session_state.current_output = {
            'tamil': tamil_translation,
            'simple_english': simple_english,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to history
        st.session_state.translation_history.append({
            'input': input_text[:100] + "..." if len(input_text) > 100 else input_text,
            'output_option': output_option,
            'time': datetime.now().strftime("%H:%M:%S")
        })

# Display results if available
if st.session_state.current_output:
    st.markdown("---")
    st.markdown("## 📊 Results")
    
    # Create columns for outputs
    if output_option == "Both Tamil & English":
        col_tamil, col_english = st.columns(2)
        
        with col_tamil:
            st.markdown("<div class='language-box'>", unsafe_allow_html=True)
            st.markdown("### 🇮🇳 Tamil Translation")
            st.write(st.session_state.current_output['tamil'])
            
            if voice_option and st.session_state.current_output['tamil']:
                audio_file = generate_tamil_audio(st.session_state.current_output['tamil'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    st.markdown(f"**Download:** {get_binary_file_downloader_html(audio_file, 'Tamil Audio')}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_english:
            st.markdown("<div class='language-box'>", unsafe_allow_html=True)
            st.markdown("### 🇬🇧 Simple English")
            st.write(st.session_state.current_output['simple_english'])
            
            if voice_option and st.session_state.current_output['simple_english']:
                audio_file = generate_english_audio(st.session_state.current_output['simple_english'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
                    st.markdown(f"**Download:** {get_binary_file_downloader_html(audio_file, 'English Audio')}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    else:  # Single language output
        st.markdown("<div class='output-box'>", unsafe_allow_html=True)
        if output_option == "Tamil Only":
            st.markdown("### 🇮🇳 Tamil Translation")
            st.write(st.session_state.current_output['tamil'])
            
            if voice_option:
                audio_file = generate_tamil_audio(st.session_state.current_output['tamil'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
        else:  # Simple English Only
            st.markdown("### 🇬🇧 Simple English")
            st.write(st.session_state.current_output['simple_english'])
            
            if voice_option:
                audio_file = generate_english_audio(st.session_state.current_output['simple_english'])
                if audio_file:
                    st.audio(audio_file, format='audio/mp3')
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate downloadable document
    if doc_option:
        st.markdown("---")
        st.markdown("### 📄 Download Options")
        
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_LEFT
        
        # Create PDF
        pdf_filename = f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        story = []
        
        # Add styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Add content
        story.append(Paragraph("Talk2Tamil Translation Result", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Original Text:", styles['Heading2']))
        story.append(Paragraph(st.session_state.original_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        if output_option in ["Tamil Only", "Both Tamil & English"]:
            story.append(Paragraph("Tamil Translation:", styles['Heading2']))
            story.append(Paragraph(st.session_state.current_output['tamil'], styles['Normal']))
            story.append(Spacer(1, 20))
        
        if output_option in ["Simple English Only", "Both Tamil & English"]:
            story.append(Paragraph("Simple English Version:", styles['Heading2']))
            story.append(Paragraph(st.session_state.current_output['simple_english'], styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Provide download link
        with open(pdf_filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        
        st.download_button(
            label="📥 Download as PDF",
            data=PDFbyte,
            file_name=pdf_filename,
            mime='application/pdf'
        )
        
        # Also offer text file download
        txt_content = f"""Talk2Tamil Translation Result
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ORIGINAL TEXT:
{st.session_state.original_text}

"""
        
        if output_option in ["Tamil Only", "Both Tamil & English"]:
            txt_content += f"""TAMIL TRANSLATION:
{st.session_state.current_output['tamil']}

"""
        
        if output_option in ["Simple English Only", "Both Tamil & English"]:
            txt_content += f"""SIMPLE ENGLISH:
{st.session_state.current_output['simple_english']}
"""
        
        st.download_button(
            label="📝 Download as Text File",
            data=txt_content,
            file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime='text/plain'
        )

# Sidebar for history and info
with st.sidebar:
    st.markdown("## 📖 Translation History")
    if st.session_state.translation_history:
        for i, item in enumerate(reversed(st.session_state.translation_history[-5:]), 1):
            st.markdown(f"{i}. **{item['output_option']}** - {item['time']}")
            st.caption(item['input'][:50] + "...")
    else:
        st.info("No translations yet. Enter text to begin!")
    
    st.markdown("---")
    st.markdown("## ℹ️ About")
    st.markdown("""
    **Talk2Tamil** helps you:
    - Translate any language to Tamil
    - Get simplified English versions
    - Listen to voice outputs
    - Download documents
    
    Perfect for:
    - Understanding bank notices
    - Reading government documents
    - Learning English simply
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Talk2Tamil - Making Information Accessible | Built for Rural India"
    "</div>",
    unsafe_allow_html=True
)
