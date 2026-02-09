"""
Phase 1: Any Language to Simple Tamil
"""

import streamlit as st
from utils import (
    translate_to_simple_tamil,
    detect_language,
    process_image_to_text,
    process_pdf_to_text,
    process_audio_to_text,
    get_example_texts
)

def show():
    """Show Phase 1 interface"""
    
    st.markdown("## 🌍 எந்த மொழியிலிருந்தும் எளிய தமிழுக்கு")
    st.markdown("Google Translate, Bhashini போன்றவற்றை விட சிறந்த மொழிபெயர்ப்பு")
    
    # Input Method Selection
    st.markdown("### 📥 உள்ளீடு முறையைத் தேர்ந்தெடுக்கவும்")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📝 உரை", use_container_width=True):
            st.session_state.input_method = "text"
    with col2:
        if st.button("🎤 குரல்", use_container_width=True):
            st.session_state.input_method = "audio"
    with col3:
        if st.button("🖼️ படம்", use_container_width=True):
            st.session_state.input_method = "image"
    with col4:
        if st.button("📄 PDF", use_container_width=True):
            st.session_state.input_method = "pdf"
    
    # Default to text input
    if 'input_method' not in st.session_state:
        st.session_state.input_method = "text"
    
    input_text = ""
    
    # Text Input
    if st.session_state.input_method == "text":
        st.markdown("#### 📝 உரையை உள்ளிடவும்")
        
        # Example buttons
        examples = get_example_texts()
        cols = st.columns(4)
        
        with cols[0]:
            if st.button("ஆங்கிலம்", use_container_width=True):
                st.session_state.demo_text = examples["english"]
        with cols[1]:
            if st.button("இந்தி", use_container_width=True):
                st.session_state.demo_text = examples["hindi"]
        with cols[2]:
            if st.button("நவீன தமிழ்", use_container_width=True):
                st.session_state.demo_text = examples["modern_tamil"]
        with cols[3]:
            if st.button("பழந்தமிழ்", use_container_width=True):
                st.session_state.demo_text = examples["ancient_tamil"]
        
        input_text = st.text_area(
            "உரையை இங்கே உள்ளிடவும்:",
            value=st.session_state.get('demo_text', examples["english"]),
            height=150,
            placeholder="எந்த மொழியிலும் உரையை உள்ளிடவும்..."
        )
    
    # Audio Input
    elif st.session_state.input_method == "audio":
        st.markdown("#### 🎤 குரல் உள்ளீடு")
        
        audio_file = st.file_uploader("குரல் கோப்பைப் பதிவேற்றவும்", type=['wav', 'mp3', 'm4a'])
        
        if audio_file:
            if st.button("குரலை உரையாக மாற்று"):
                with st.spinner("குரல் செயலாக்கப்படுகிறது..."):
                    input_text = process_audio_to_text(audio_file)
                    st.text_area("பிரித்தெடுக்கப்பட்ட உரை:", input_text, height=100)
    
    # Image Input
    elif st.session_state.input_method == "image":
        st.markdown("#### 🖼️ படம் பதிவேற்றம்")
        
        image_file = st.file_uploader("படத்தைப் பதிவேற்றவும்", type=['png', 'jpg', 'jpeg'])
        
        if image_file:
            from PIL import Image
            image = Image.open(image_file)
            st.image(image, caption="பதிவேற்றப்பட்ட படம்", use_column_width=True)
            
            if st.button("படத்திலிருந்து உரையைப் பிரித்தெடுக்கவும்"):
                with st.spinner("படம் செயலாக்கப்படுகிறது..."):
                    input_text = process_image_to_text(image)
                    st.text_area("பிரித்தெடுக்கப்பட்ட உரை:", input_text, height=100)
    
    # PDF Input
    elif st.session_state.input_method == "pdf":
        st.markdown("#### 📄 PDF பதிவேற்றம்")
        
        pdf_file = st.file_uploader("PDF கோப்பைப் பதிவேற்றவும்", type=['pdf'])
        
        if pdf_file:
            if st.button("PDF இலிருந்து உரையைப் பிரித்தெடுக்கவும்"):
                with st.spinner("PDF செயலாக்கப்படுகிறது..."):
                    input_text = process_pdf_to_text(pdf_file)
                    st.text_area("பிரித்தெடுக்கப்பட்ட உரை:", input_text, height=150)
    
    # Process Button
    if input_text and st.button("✨ தமிழாக மாற்று", type="primary", use_container_width=True):
        with st.spinner("மொழிபெயர்ப்பு செயல்படுத்தப்படுகிறது..."):
            
            # Detect language
            detected_lang = detect_language(input_text)
            
            # Translate to simple Tamil
            simple_tamil = translate_to_simple_tamil(input_text)
            
            # Display results
            st.markdown("---")
            st.markdown("## 📊 முடிவுகள்")
            
            # Language info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("கண்டறியப்பட்ட மொழி", detected_lang)
            with col2:
                st.metric("உள்ளீட்டு நீளம்", f"{len(input_text.split())} சொற்கள்")
            with col3:
                st.metric("மொழிபெயர்ப்பு நிலை", "முடிந்தது")
            
            # Comparison with Google Translate
            st.markdown("### 🔄 எங்கள் மொழிபெயர்ப்பு vs Google Translate")
            
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.markdown("#### 🤖 Google Translate (உதாரணம்)")
                # Simulated Google Translate output
                google_translate = "கல்வி என்பது உலகத்தை மாற்றுவதற்கு நீங்கள் பயன்படுத்தக்கூடிய மிகவும் சக்திவாய்ந்த ஆயுதமாகும்."
                st.markdown(f'<div class="tamil-text-box">{google_translate}</div>', unsafe_allow_html=True)
                st.caption("முறையான, கடினமான தமிழ்")
            
            with comp_col2:
                st.markdown("#### ✨ எங்கள் எளிய தமிழ்")
                st.markdown(f'<div class="simple-tamil-box">{simple_tamil}</div>', unsafe_allow_html=True)
                st.caption("எளிதில் புரியும், பேச்சுத் தமிழ்")
            
            # Why our translation is better
            st.markdown("### 👍 எங்கள் மொழிபெயர்ப்பு ஏன் சிறந்தது?")
            
            improvement_points = [
                "✅ **சூழல்-அறிந்த மொழிபெயர்ப்பு:** வாக்கியத்தின் பொருளைப் புரிந்துகொண்டு மொழிபெயர்க்கிறது",
                "✅ **பேச்சுத் தமிழ்:** முறையான தமிழுக்கு பதிலாக பேச்சுத் தமிழைப் பயன்படுத்துகிறது",
                "✅ **குறுகிய வாக்கியங்கள்:** நீண்ட வாக்கியங்களை சிறியதாகப் பிரிக்கிறது",
                "✅ **பொதுச் சொற்கள்:** கடினமான சொற்களை எளிமையானவற்றால் மாற்றுகிறது",
                "✅ **மாணவர்-நட்பு:** பள்ளி மாணவர்கள் எளிதாகப் புரிந்துகொள்ளும் வகையில்"
            ]
            
            for point in improvement_points:
                st.markdown(point)
            
            # Download option
            st.download_button(
                label="📥 மொழிபெயர்ப்பைப் பதிவிறக்குக",
                data=simple_tamil,
                file_name="எளிய_தமிழ்_மொழிபெயர்ப்பு.txt",
                mime="text/plain",
                use_container_width=True
            )
