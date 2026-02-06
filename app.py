import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import os

# Set page config
st.set_page_config(
    page_title="Ancient Tamil Inscription Converter",
    page_icon="📜",
    layout="wide"
)

# Check if Tesseract is installed (you might need to install it separately)
# For Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# For Linux/Mac: sudo apt-get install tesseract-ocr or brew install tesseract

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #A23B72;
        margin-top: 20px;
    }
    .success-box {
        background-color: #D4EDDA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #155724;
    }
    .warning-box {
        background-color: #FFF3CD;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #856404;
    }
    .info-box {
        background-color: #E7F3FF;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #004085;
    }
    .tamil-font {
        font-family: 'Arial Unicode MS', 'Latha', 'Koodal', 'TAMu_Kadambri', sans-serif;
        font-size: 1.2rem;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📜 Ancient Tamil Inscription Converter</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <strong>Project Goal:</strong> Convert ancient Tamil inscriptions (from stones, copper plates, etc.) 
    into modern Tamil language for archaeological research.
</div>
""", unsafe_allow_html=True)

# Sidebar for instructions and info
with st.sidebar:
    st.header("📖 Instructions")
    st.markdown("""
    1. **Upload an image** of a Tamil inscription (stone, copper plate, palm leaf)
    2. The app will extract text using OCR
    3. View the extracted text and conversion results
    4. **Note:** For best results:
       - Use clear, high-resolution images
       - Ensure good lighting and contrast
       - Crop to the inscription area if possible
    """)
    
    st.markdown("---")
    
    st.header("🔍 Supported Scripts")
    st.markdown("""
    - **Tamil-Brahmi** (300 BCE - 300 CE)
    - **Vatteluttu** (4th-10th century CE)
    - **Early Tamil script** (Chola period)
    - **Modern Tamil** (comparison)
    """)
    
    st.markdown("---")
    
    st.header("⚠️ Limitations")
    st.markdown("""
    - OCR accuracy depends on image quality
    - Ancient scripts may need manual correction
    - Some archaic words require expert interpretation
    """)

# Ancient to Modern Tamil character mapping (simplified example)
# In a real implementation, you'd need a comprehensive mapping
TAMIL_CHAR_MAPPING = {
    # Ancient Tamil-Brahmi to Modern Tamil (example mappings)
    '𑀓': 'க', '𑀔': 'க', '𑀕': 'க',
    '𑀖': 'க', '𑀗': 'ங', '𑀘': 'ச',
    '𑀙': 'ச', '𑀚': 'ஜ', '𑀛': 'ஜ',
    '𑀝': 'ட', '𑀞': 'ட', '𑀟': 'ட',
    '𑀠': 'ட', '𑀡': 'ண', '𑀢': 'த',
    '𑀣': 'த', '𑀤': 'த', '𑀥': 'த',
    '𑀦': 'ந', '𑀧': 'ப', '𑀨': 'ப',
    '𑀩': 'ப', '𑀪': 'ப', '𑀫': 'ம',
    '𑀬': 'ய', '𑀭': 'ர', '𑀮': 'ல',
    '𑀯': 'வ', '𑀰': 'ஷ', '𑀱': 'ஷ',
    '𑀲': 'ச', '𑀳': 'ஹ', '𑀴': 'ள',
    '𑀵': 'ற', '𑀶': 'ன',
    
    # Vatteluttu to Modern Tamil (example)
    '𑍐': 'ஐ', '𑍑': 'ஒ', '𑍒': 'ஓ',
    
    # Some common ancient forms (hypothetical examples)
    '௧': '¹', '௨': '²', '௩': '³',  # Ancient numbers
}

# Sample ancient Tamil words and their modern equivalents
ANCIENT_WORDS_DB = {
    '𑀓𑁂𑀭𑀮': 'கேரள',
    '𑀘𑁂𑀭': 'சேர',
    '𑀧𑀸𑀢𑀮': 'பாடல்',
    '𑀫𑀸𑀢𑀮': 'மாடல்',
    '𑀢𑀭𑀲': 'தரசு',
    '𑀯𑀸𑀮': 'வால்',
    '𑀫𑁂𑀬𑀓𑀻𑀭𑁆𑀢𑀺': 'மெய்கீர்த்தி',
    '𑀆𑀦𑀺': 'ஆணி',
}

def preprocess_image(image):
    """Preprocess image for better OCR results"""
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    
    # Convert to grayscale
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.medianBlur(thresh, 3)
    
    return Image.fromarray(denoised)

def extract_text_with_ocr(image):
    """Extract text from image using Tesseract OCR"""
    try:
        # Try with Tamil language first
        custom_config = r'--oem 3 --psm 6 -l tam'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        if not text.strip():
            # If no text found with Tamil, try without language specification
            text = pytesseract.image_to_string(image)
        
        return text.strip()
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        st.info("Make sure Tesseract OCR is installed on your system.")
        return ""

def convert_to_modern_tamil(text):
    """Convert ancient Tamil characters to modern Tamil"""
    converted_text = ""
    for char in text:
        # Check if character is in our mapping
        if char in TAMIL_CHAR_MAPPING:
            converted_text += TAMIL_CHAR_MAPPING[char]
        else:
            converted_text += char
    
    # Try to match with known ancient words
    for ancient_word, modern_word in ANCIENT_WORDS_DB.items():
        if ancient_word in converted_text:
            converted_text = converted_text.replace(ancient_word, modern_word)
    
    return converted_text

def analyze_text(text):
    """Analyze extracted text and provide insights"""
    analysis = {
        "character_count": len(text),
        "word_count": len(text.split()),
        "tamil_characters": sum(1 for char in text if '\u0B80' <= char <= '\u0BFF'),
        "ancient_characters": sum(1 for char in text if char in TAMIL_CHAR_MAPPING),
    }
    return analysis

# Main app layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="sub-header">📤 Upload Inscription Image</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Upload a clear image of the Tamil inscription"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Inscription Image", use_column_width=True)
        
        # Preprocessing options
        with st.expander("🛠️ Image Processing Options"):
            enhance = st.checkbox("Enhance image for better OCR", value=True)
            show_processed = st.checkbox("Show processed image", value=False)
            
            if enhance:
                processed_image = preprocess_image(image)
                if show_processed:
                    st.image(processed_image, caption="Processed Image", use_column_width=True)
            else:
                processed_image = image
        
        # Process button
        if st.button("🔍 Extract and Convert Text", type="primary", use_container_width=True):
            with st.spinner("Processing inscription..."):
                # Extract text using OCR
                extracted_text = extract_text_with_ocr(processed_image)
                
                if extracted_text:
                    # Convert to modern Tamil
                    modern_text = convert_to_modern_tamil(extracted_text)
                    
                    # Analyze text
                    analysis = analyze_text(extracted_text)
                    
                    # Store in session state
                    st.session_state['extracted_text'] = extracted_text
                    st.session_state['modern_text'] = modern_text
                    st.session_state['analysis'] = analysis
                    
                    st.success("✅ Text extracted successfully!")
                else:
                    st.warning("⚠️ No text could be extracted. Try a clearer image.")

with col2:
    st.markdown('<h2 class="sub-header">📝 Conversion Results</h2>', unsafe_allow_html=True)
    
    if 'extracted_text' in st.session_state:
        # Display analysis
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**Analysis:**")
        st.markdown(f"- Characters detected: {st.session_state['analysis']['character_count']}")
        st.markdown(f"- Tamil characters: {st.session_state['analysis']['tamil_characters']}")
        st.markdown(f"- Ancient characters found: {st.session_state['analysis']['ancient_characters']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["🔄 Side-by-Side", "📜 Original", "🆕 Modern"])
        
        with tab1:
            st.markdown('<div class="tamil-font">', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Original Extracted Text:**")
                st.text_area("", st.session_state['extracted_text'], height=200, disabled=True, label_visibility="collapsed")
            
            with col_b:
                st.markdown("**Converted Modern Tamil:**")
                st.text_area("", st.session_state['modern_text'], height=200, disabled=True, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="warning-box tamil-font">', unsafe_allow_html=True)
            st.markdown("**Original Text (OCR Output):**")
            st.write(st.session_state['extracted_text'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="success-box tamil-font">', unsafe_allow_html=True)
            st.markdown("**Modern Tamil Conversion:**")
            st.write(st.session_state['modern_text'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Download options
        st.markdown("---")
        st.markdown("### 💾 Download Results")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            # Create downloadable text file
            result_text = f"""Ancient Tamil Inscription Analysis
====================================

Original Text (OCR):
{st.session_state['extracted_text']}

Modern Tamil Conversion:
{st.session_state['modern_text']}

Analysis:
- Total characters: {st.session_state['analysis']['character_count']}
- Tamil characters: {st.session_state['analysis']['tamil_characters']}
- Ancient characters: {st.session_state['analysis']['ancient_characters']}

Generated by Ancient Tamil Inscription Converter
"""
            st.download_button(
                label="📥 Download as Text",
                data=result_text,
                file_name="tamil_inscription_results.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_d2:
            # Save as CSV
            df = pd.DataFrame({
                'Original': [st.session_state['extracted_text']],
                'Modern_Tamil': [st.session_state['modern_text']],
                'Character_Count': [st.session_state['analysis']['character_count']],
                'Tamil_Chars': [st.session_state['analysis']['tamil_characters']]
            })
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download as CSV",
                data=csv,
                file_name="tamil_inscription_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Manual correction option
        with st.expander("✏️ Manual Correction & Notes"):
            corrected_text = st.text_area(
                "Correct the modern Tamil text if needed:",
                st.session_state['modern_text'],
                height=150
            )
            notes = st.text_area("Archaeological notes and observations:", height=100)
            
            if st.button("Save Corrections"):
                st.session_state['modern_text'] = corrected_text
                st.session_state['notes'] = notes
                st.success("Corrections saved!")
    
    else:
        st.info("👈 Upload an image and click 'Extract and Convert Text' to see results here.")
        st.markdown("---")
        
        # Show sample conversion
        st.markdown("### 🧪 Sample Conversion")
        sample_ancient = "𑀓𑁂𑀭𑀮 𑀘𑁂𑀭 𑀫𑁂𑀬𑀓𑀻𑀭𑁆𑀢𑀺"
        sample_modern = convert_to_modern_tamil(sample_ancient)
        
        st.markdown(f"**Ancient:** {sample_ancient}")
        st.markdown(f"**Modern:** {sample_modern}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>Ancient Tamil Inscription Converter</strong> | For Archaeological Research</p>
    <p>Note: This is a prototype. For professional epigraphy, consult with experts from 
    Department of Archaeology, Tamil University, or similar institutions.</p>
</div>
""", unsafe_allow_html=True)

# Instructions for running the app
with st.expander("🚀 How to Run This App"):
    st.markdown("""
    1. **Install requirements:**
       ```bash
       pip install -r requirements.txt
       ```
    
    2. **Install Tesseract OCR:**
       - **Windows:** Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
       - **Linux:** `sudo apt-get install tesseract-ocr tesseract-ocr-tam`
       - **Mac:** `brew install tesseract tesseract-lang`
    
    3. **Run the app:**
       ```bash
       streamlit run app.py
       ```
    
    4. **For better accuracy:**
       - Train Tesseract with ancient Tamil fonts
       - Use high-quality images
       - Consider manual verification
    """)

