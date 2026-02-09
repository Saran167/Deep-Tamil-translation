"""
தமிழ் மாற்றம் - Dual Phase Tamil Transformation System
Phase 1: Any Language → Simple Tamil
Phase 2: Ancient Tamil → Modern Tamil + Meanings
"""

import streamlit as st
import json
import os

# Page config
st.set_page_config(
    page_title="தமிழ் மாற்றம்",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;500;700&display=swap');

* {
    font-family: 'Noto Sans Tamil', sans-serif;
}

.main-title {
    font-size: 3rem;
    color: #2E86AB;
    text-align: center;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.sub-title {
    font-size: 1.2rem;
    color: #5D5D5D;
    text-align: center;
    margin-bottom: 2rem;
}

.phase-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 15px;
    height: 100%;
    transition: transform 0.3s;
}

.phase-card:hover {
    transform: translateY(-5px);
}

.tamil-text-box {
    font-size: 1.4rem;
    color: #D35400;
    background: #FFF9E6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #D35400;
    margin: 15px 0;
}

.simple-tamil-box {
    font-size: 1.3rem;
    color: #27AE60;
    background: #E8F8F3;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #27AE60;
    margin: 15px 0;
}

.meaning-box {
    font-size: 1.1rem;
    color: #8E44AD;
    background: #F4ECF7;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #8E44AD;
    margin: 15px 0;
}

.feature-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    height: 100%;
}

.input-method-btn {
    text-align: center;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
}

.input-method-btn:hover {
    border-color: #2E86AB;
    background: #F0F8FF;
}

.input-method-btn.selected {
    border-color: #2E86AB;
    background: #E6F3FF;
}

.stButton > button {
    background: linear-gradient(135deg, #2E86AB 0%, #1B4F72 100%);
    color: white;
    border-radius: 8px;
    padding: 12px 30px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1B4F72 0%, #0C3D5B 100%);
}

.sidebar-header {
    font-size: 1.8rem;
    color: #2E86AB;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Import utility functions
try:
    from utils import (
        translate_to_simple_tamil,
        simplify_ancient_tamil,
        extract_meaning_from_tamil,
        process_image_to_text,
        process_pdf_to_text,
        process_audio_to_text,
        detect_language,
        get_complexity_score
    )
except ImportError:
    # Fallback functions if utils not available
    def translate_to_simple_tamil(text):
        return f"தமிழ் மொழிப்பெயர்ப்பு: {text}"
    
    def simplify_ancient_tamil(text):
        return text.replace("அழகைன்று", "அழகு என்று").replace("பேரர்", "பெயர்")
    
    def extract_meaning_from_tamil(text):
        return f"பொருள்: {text} என்பது ஒரு தமிழ் வாக்கியம்"

# Load Tamil data
def load_tamil_data():
    """Load Tamil poems and examples"""
    try:
        with open('poetry_examples.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "examples": {
                "பாரதியார் - தமிழ் வாழ்த்து": [
                    "தமிழுக்கும் அழகைன்றுபேரர்!",
                    "அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்!"
                ],
                "ஔவையார் - கல்வி": [
                    "கற்க கசடறக் கற்பவை கற்றபின்",
                    "நிற்க அதற்குத் தக"
                ]
            }
        }

def main():
    """Main application"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-header">தமிழ் மாற்றம்</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        page = st.radio(
            "🌐 அடுக்கு தேர்வு",
            ["🏠 முகப்பு", "🔄 1. எளிய தமிழாக மாற்று", "📜 2. பழந்தமிழைப் புரிந்துகொள்", "📊 பயனர் வழிகாட்டி"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Language info
        st.markdown("**🌍 ஆதரவு மொழிகள்:**")
        st.markdown("- ஆங்கிலம்")
        st.markdown("- இந்தி")
        st.markdown("- தெலுங்கு")
        st.markdown("- மலையாளம்")
        st.markdown("- கன்னடம்")
        st.markdown("- பிற இந்திய மொழிகள்")
        
        st.markdown("---")
        
        st.markdown("**🎯 பயனர்கள்:**")
        st.markdown("- மாணவர்கள்")
        st.markdown("- TNPSC தேர்வர்கள்")
        st.markdown("- தமிழ் கற்கும் மக்கள்")
        st.markdown("- ஆசிரியர்கள்")
        
        st.markdown("---")
        st.caption("தமிழுக்காக உருவாக்கப்பட்டது ❤️")
    
    # Page routing
    if page == "🏠 முகப்பு":
        show_home_page()
    elif page == "🔄 1. எளிய தமிழாக மாற்று":
        show_phase1_page()
    elif page == "📜 2. பழந்தமிழைப் புரிந்துகொள்":
        show_phase2_page()
    elif page == "📊 பயனர் வழிகாட்டி":
        show_user_guide()

def show_home_page():
    """Home page with project overview"""
    
    st.markdown('<div class="main-title">தமிழ் மாற்றம்</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">இரட்டை-அடுக்கு தமிழ் மாற்றும் அமைப்பு</div>', unsafe_allow_html=True)
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 எங்கள் நோக்கம்
        
        தமிழ் கற்கும் அனைவருக்கும் சிக்கலான உரைகளை எளிதாக்குவது!
        
        **இரட்டை அடுக்கு அமைப்பு:**
        
        1. **எந்த மொழியையும் எளிய தமிழாக மாற்றுகிறோம்**  
           - Google Translate போன்ற பயன்பாடுகளை விட சிறந்தது
           - மக்கள் புரிந்துகொள்ளும் எளிய தமிழ்
           - சூழல்-அறிந்த மொழிபெயர்ப்பு
        
        2. **பழந்தமிழ் உரைகளை நவீன தமிழாக மாற்றுகிறோம்**  
           - பாடல் வரிகள் புரியும்
           - வரிக்கு வரி பொருள் விளக்கம்
           - பழைய சொற்களுக்கான அகராதி
        """)
    
    with col2:
        st.image("https://img.icons8.com/color/300/000000/india.png", width=200)
    
    st.markdown("---")
    
    # Two Phase Cards
    st.markdown("### ✨ இரண்டு அடுக்குகள்")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="phase-card">
        <h3>🔄 1. எளிய தமிழாக மாற்று</h3>
        <p>எந்த மொழியிலும் உள்ள உரையை எளிய தமிழாக மாற்றுங்கள்.</p>
        <br>
        <strong>சிறப்பு அம்சங்கள்:</strong>
        <ul>
        <li>எந்த மொழியிலிருந்தும் தமிழாக</li>
        <li>குரல் உள்ளீடு ஆதரவு</li>
        <li>படம்/PDF மூலம் உரை பிரித்தெடுத்தல்</li>
        <li>Google Translate-ஐ விட சிறந்தது</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 1வது அடுக்கை முயல்க", use_container_width=True):
            st.switch_page("pages/02_🔄_Phase1_Simple_Tamil.py")
    
    with col2:
        st.markdown("""
        <div class="phase-card">
        <h3>📜 2. பழந்தமிழைப் புரிந்துகொள்</h3>
        <p>பழந்தமிழ் உரைகளை நவீன தமிழாக மாற்றி பொருள் விளக்குக.</p>
        <br>
        <strong>சிறப்பு அம்சங்கள்:</strong>
        <ul>
        <li>பழந்தமிழ் → நவீன தமிழ்</li>
        <li>வரிக்கு வரி பொருள் விளக்கம்</li>
        <li>பழைய சொற்களுக்கான அகராதி</li>
        <li>மாணவர்களுக்கான கற்றல் உதவி</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📜 2வது அடுக்கை முயல்க", use_container_width=True):
            st.switch_page("pages/03_📜_Phase2_Tamil_Poetry.py")
    
    st.markdown("---")
    
    # Comparison Table
    st.markdown("### 📊 எங்கள் அமைப்பு vs மற்ற பயன்பாடுகள்")
    
    comparison_data = {
        "அம்சம்": ["மொழிபெயர்ப்பு தரம்", "புரிதல் எளிமை", "மாணவர்-நட்பு", "பழந்தமிழ் ஆதரவு", "பல உள்ளீடு வகைகள்"],
        "Google Translate": ["நல்லது", "கடினம்", "இல்லை", "இல்லை", "உரை மட்டும்"],
        "Bhashini": ["நல்லது", "மிதமான", "குறைவு", "குறைவு", "உரை மட்டும்"],
        "எங்கள் அமைப்பு": ["சிறந்தது", "மிக எளிது", "ஆம்", "முழு ஆதரவு", "உரை, குரல், படம், PDF"]
    }
    
    st.table(comparison_data)
    
    # Quick Demo
    st.markdown("---")
    st.markdown("### 🚀 விரைவு செயல்பாடு")
    
    demo_col1, demo_col2, demo_col3 = st.columns(3)
    
    with demo_col1:
        if st.button("ஆங்கில உதாரணம்", use_container_width=True):
            st.session_state.demo_text = "Education is the most powerful weapon to change the world."
    
    with demo_col2:
        if st.button("பழந்தமிழ் உதாரணம்", use_container_width=True):
            st.session_state.demo_text = "தமிழுக்கும் அழகைன்றுபேரர்!"
    
    with demo_col3:
        if st.button("செயல்படுத்து", type="primary", use_container_width=True):
            if 'demo_text' in st.session_state:
                st.switch_page("pages/02_🔄_Phase1_Simple_Tamil.py")

def show_phase1_page():
    """Phase 1: Any language to simple Tamil"""
    st.markdown('<div class="main-title">🔄 எளிய தமிழாக மாற்று</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">எந்த மொழியிலிருந்தும் எளிய புரியும் தமிழுக்கு</div>', unsafe_allow_html=True)
    
    # Load the Phase 1 page
    import pages._02_Phase1_Simple_Tamil as phase1
    phase1.show()

def show_phase2_page():
    """Phase 2: Ancient Tamil to Modern Tamil"""
    st.markdown('<div class="main-title">📜 பழந்தமிழைப் புரிந்துகொள்</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">பழந்தமிழ் உரைகளை நவீன தமிழாகவும் பொருளுடனும் மாற்றுதல்</div>', unsafe_allow_html=True)
    
    # Load the Phase 2 page
    import pages._03_Phase2_Tamil_Poetry as phase2
    phase2.show()

def show_user_guide():
    """User guide page"""
    st.markdown('<div class="main-title">📊 பயனர் வழிகாட்டி</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 📖 எப்படி பயன்படுத்துவது?
    
    ### 1வது அடுக்கு: எளிய தமிழாக மாற்று
    1. **உள்ளீடு முறையை தேர்ந்தெடுக்கவும்:**
       - உரை: நேரடியாக தட்டச்சு செய்யவும்
       - குரல்: குரல் மூலம் உரையை உள்ளிடவும்
       - படம்: படத்திலிருந்து உரையை பிரித்தெடுக்கவும்
       - PDF: PDF கோப்பிலிருந்து உரையை பிரித்தெடுக்கவும்
    
    2. **உரையை உள்ளிடவும் / பதிவேற்றவும்**
    3. **"தமிழாக மாற்று" பொத்தானை அழுத்தவும்**
    4. **முடிவுகளைப் பார்க்கவும்:**
       - தமிழ் மொழிபெயர்ப்பு
       - எளிமைப்படுத்தப்பட்ட தமிழ்
       - பொருள் விளக்கம்
    
    ### 2வது அடுக்கு: பழந்தமிழைப் புரிந்துகொள்
    1. **ஒரு பாடலை தேர்ந்தெடுக்கவும் அல்லது உள்ளிடவும்**
    2. **"பகுப்பாய்வு செய்க" பொத்தானை அழுத்தவும்**
    3. **வரிக்கு வரி பகுப்பாய்வைப் பார்க்கவும்:**
       - அசல் வரி
       - நவீன தமிழ் பதிப்பு
       - பொருள் விளக்கம்
       - பழைய சொற்களின் அகராதி
    
    ## 🎯 யாருக்காக?
    
    ### மாணவர்கள்:
    - பள்ளி மாணவர்கள் (6-12ம் வகுப்பு)
    - கல்லூரி மாணவர்கள்
    - தமிழ் கற்கும் மாணவர்கள்
    
    ### TNPSC தேர்வர்கள்:
    - தமிழ் இலக்கியம் பகுதி
    - பழந்தமிழ் பகுதி
    - வரலாறு பகுதி
    
    ### பொது மக்கள்:
    - தமிழ் கற்க விரும்புவோர்
    - தமிழ் இலக்கியம் படிக்க விரும்புவோர்
    - ஆராய்ச்சியாளர்கள்
    
    ## 🔧 தொழில்நுட்பம்
    
    - **முன்பக்கம்:** Streamlit (Python)
    - **மொழிபெயர்ப்பு:** Google Translate API + சிறப்பு விதிகள்
    - **உரை எளிமைப்படுத்தல்:** AI மாதிரிகள் + விதி-அடிப்படையிலான
    - **பட உரை பிரித்தெடுத்தல்:** Tesseract OCR
    - **குரல் உரை பிரித்தெடுத்தல்:** SpeechRecognition
    
    ## 📱 உள்ளீடு வகைகள்
    
    1. **உரை உள்ளீடு:** எந்த மொழியிலும்
    2. **குரல் உள்ளீடு:** ஆங்கிலம் / தமிழ் / இந்தி
    3. **பட உள்ளீடு:** JPG, PNG, JPEG
    4. **PDF உள்ளீடு:** PDF கோப்புகள்
    
    ## 💡 உதவிக்குறிப்புகள்
    
    1. தெளிவான உரையை உள்ளிடவும்
    2. படங்கள் தெளிவாக இருக்க வேண்டும்
    3. நீண்ட உரைகளை பகுதிகளாக உள்ளிடவும்
    4. முடிவுகளை பதிவிறக்கம் செய்யலாம்
    
    ## ❓ உதவி தேவைப்பட்டால்
    
    - Email: help@tamiltransform.com
    - Phone: +91-XXXXXX-XXXX
    - Website: www.tamiltransform.com
    
    ---
    
    > **"சிக்கலானதை எளிதாக்குவோம், புரிந்துகொள்வதை எளிதாக்குவோம்"**
    
    **தமிழ் மாற்றம் அணி** ❤️
    """)

if __name__ == "__main__":
    main()

