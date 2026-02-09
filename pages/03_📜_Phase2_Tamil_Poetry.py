"""
Phase 2: Ancient Tamil to Modern Tamil with Meanings
"""

import streamlit as st
import json
from utils import (
    simplify_ancient_tamil,
    get_example_texts,
    process_image_to_text,
    process_pdf_to_text
)

def load_poetry_database():
    """Load Tamil poetry database"""
    try:
        with open('poetry_examples.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "பாரதியார் - தமிழ் வாழ்த்து": {
                "period": "நவீன காலம்",
                "lines": [
                    "தமிழுக்கும் அழகைன்றுபேரர்!",
                    "அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்!",
                    "தமிழுக்கு நிலவென்று பேரர்!",
                    "இன்பத் தமிழ் எங்கள் சமூகத்தின் விளைவுக்கு நீர்!",
                    "தமிழுக்கு மணமென்று பேரர்!",
                    "இன்பத் தமிழ் எங்கள் வாழ்வுக்கு நிருமித்த ஊர்!"
                ]
            },
            "ஔவையார் - கல்வி": {
                "period": "சங்க காலம்",
                "lines": [
                    "கற்க கசடறக் கற்பவை கற்றபின்",
                    "நிற்க அதற்குத் தக"
                ]
            }
        }

def show():
    """Show Phase 2 interface"""
    
    st.markdown("## 📜 பழந்தமிழ் → நவீன தமிழ் + பொருள்")
    st.markdown("மாணவர்கள், TNPSC தேர்வர்களுக்கான சிறப்பு கற்றல் கருவி")
    
    # Input Method Selection
    st.markdown("### 📥 உள்ளீடு முறை")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 உரை உள்ளீடு", use_container_width=True):
            st.session_state.input_method = "text"
    with col2:
        if st.button("📖 பாடல் தேர்வு", use_container_width=True):
            st.session_state.input_method = "poem"
    with col3:
        if st.button("📄 கோப்பு பதிவேற்றம்", use_container_width=True):
            st.session_state.input_method = "file"
    
    if 'input_method' not in st.session_state:
        st.session_state.input_method = "text"
    
    input_text = ""
    lines = []
    
    # Text Input
    if st.session_state.input_method == "text":
        st.markdown("#### 📝 பழந்தமிழ் உரையை உள்ளிடவும்")
        
        examples = get_example_texts()
        input_text = st.text_area(
            "பழந்தமிழ் உரை:",
            value=examples["ancient_tamil"],
            height=150,
            placeholder="பழந்தமிழ் உரையை இங்கே ஒட்டவும்..."
        )
        
        if input_text:
            lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    
    # Poem Selection
    elif st.session_state.input_method == "poem":
        st.markdown("#### 📖 பாடலைத் தேர்ந்தெடுக்கவும்")
        
        poems_db = load_poetry_database()
        poem_choice = st.selectbox("பாடல்:", list(poems_db.keys()))
        
        if poem_choice:
            poem = poems_db[poem_choice]
            st.markdown(f"**காலம்:** {poem['period']}")
            
            lines = poem['lines']
            
            # Show original poem
            st.markdown("**அசல் பாடல்:**")
            for line in lines:
                st.markdown(f'<div class="tamil-text-box">{line}</div>', unsafe_allow_html=True)
    
    # File Upload
    elif st.session_state.input_method == "file":
        st.markdown("#### 📄 கோப்பைப் பதிவேற்றவும்")
        
        file_type = st.radio("கோப்பு வகை:", ["🖼️ படம்", "📄 PDF"], horizontal=True)
        
        uploaded_file = st.file_uploader(
            "கோப்பைப் பதிவேற்றவும்",
            type=['png', 'jpg', 'jpeg', 'pdf']
        )
        
        if uploaded_file:
            if file_type == "🖼️ படம்":
                from PIL import Image
                image = Image.open(uploaded_file)
                st.image(image, caption="பதிவேற்றப்பட்ட படம்", use_column_width=True)
                
                if st.button("படத்திலிருந்து உரையைப் பிரித்தெடுக்கவும்"):
                    with st.spinner("படம் செயலாக்கப்படுகிறது..."):
                        input_text = process_image_to_text(image)
                        st.text_area("பிரித்தெடுக்கப்பட்ட உரை:", input_text, height=100)
                        lines = [line.strip() for line in input_text.split('\n') if line.strip()]
            
            else:  # PDF
                if st.button("PDF இலிருந்து உரையைப் பிரித்தெடுக்கவும்"):
                    with st.spinner("PDF செயலாக்கப்படுகிறது..."):
                        input_text = process_pdf_to_text(uploaded_file)
                        st.text_area("பிரித்தெடுக்கப்பட்ட உரை:", input_text, height=150)
                        lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    
    # Process Button
    if lines and st.button("🔍 பகுப்பாய்வு செய்க", type="primary", use_container_width=True):
        with st.spinner("பழந்தமிழ் பகுப்பாய்வு செயல்படுத்தப்படுகிறது..."):
            
            st.markdown("---")
            st.markdown("## 📚 வரிக்கு வரி பகுப்பாய்வு")
            
            for i, line in enumerate(lines):
                if line.strip():
                    st.markdown(f"### 📖 வரி {i+1}")
                    
                    # Analyze the line
                    analysis = simplify_ancient_tamil(line)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**அசல் வரி:**")
                        st.markdown(f'<div class="tamil-text-box">{analysis["original"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**நவீன தமிழ்:**")
                        st.markdown(f'<div class="simple-tamil-box">{analysis["modern"]}</div>', unsafe_allow_html=True)
                    
                    # Meaning
                    st.markdown("**📝 பொருள்:**")
                    st.markdown(f'<div class="meaning-box">{analysis["meaning"]}</div>', unsafe_allow_html=True)
                    
                    # Difficult words if any
                    if analysis['difficult_words']:
                        with st.expander("📖 பழைய சொற்களின் அகராதி"):
                            for word_info in analysis['difficult_words']:
                                st.markdown(f"**{word_info['word']}** → {word_info['modern']}")
                                st.markdown(f"*பொருள்:* {word_info['meaning']}")
                                st.markdown("---")
                    
                    st.markdown("---")
            
            # Educational Tips
            st.markdown("### 💡 கற்றல் உதவிக்குறிப்புகள்")
            
            tips = [
                "📚 **தினமும் சில வரிகளை மட்டும் படிக்கவும்** - மனதில் பதியும்",
                "✍️ **நோட்புக்கில் எழுதவும்** - நினைவாற்றலை அதிகரிக்கும்",
                "🗣️ **சத்தமாக வாசிக்கவும்** - உச்சரிப்பு மேம்படும்",
                "🤔 **பொருளைப் புரிந்துகொள்ள முயலவும்** - மனப்பாடம் செய்ய வேண்டாம்",
                "🔄 **மீண்டும் மீண்டும் படிக்கவும்** - பழையவை மறக்காமல் இருக்க"
            ]
            
            for tip in tips:
                st.markdown(tip)
            
            # Download all results
            result_text = "பழந்தமிழ் பகுப்பாய்வு - முடிவுகள்\n\n"
            for i, line in enumerate(lines):
                analysis = simplify_ancient_tamil(line)
                result_text += f"வரி {i+1}:\n"
                result_text += f"அசல்: {analysis['original']}\n"
                result_text += f"நவீன: {analysis['modern']}\n"
                result_text += f"பொருள்: {analysis['meaning']}\n\n"
            
            st.download_button(
                label="📥 அனைத்து முடிவுகளையும் பதிவிறக்குக",
                data=result_text,
                file_name="பழந்தமிழ்_பகுப்பாய்வு.txt",
                mime="text/plain",
                use_container_width=True
            )
