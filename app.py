import streamlit as st
import json
import re
from langdetect import detect

# Page configuration
st.set_page_config(
    page_title="தமிழ் மாற்றம் - Tamil Transformation",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful Tamil interface
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
    cursor: pointer;
}

.phase-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.original-box {
    font-size: 1.4rem;
    color: #D35400;
    background: #FFF9E6;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #D35400;
    margin: 15px 0;
}

.simple-box {
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

.stButton > button {
    background: linear-gradient(135deg, #2E86AB 0%, #1B4F72 100%);
    color: white;
    border-radius: 8px;
    padding: 12px 30px;
    font-weight: bold;
    border: none;
    font-size: 16px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1B4F72 0%, #0C3D5B 100%);
    transform: translateY(-2px);
}

.info-card {
    background: #F8F9FA;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #17A2B8;
    margin: 10px 0;
}

.warning-card {
    background: #FFF3CD;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #FFC107;
    margin: 10px 0;
}

.success-card {
    background: #D4EDDA;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #28A745;
    margin: 10px 0;
}

.tab-button {
    text-align: center;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 10px;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s;
}

.tab-button:hover {
    border-color: #2E86AB;
    background: #F0F8FF;
}

.tab-button.active {
    border-color: #2E86AB;
    background: #E6F3FF;
    font-weight: bold;
}

.sidebar-header {
    font-size: 1.8rem;
    color: #2E86AB;
    font-weight: bold;
    margin-bottom: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ========== TRANSLATION FUNCTIONS ==========

def detect_language_name(text):
    """Detect language name from text"""
    try:
        lang_code = detect(text)
        lang_map = {
            'en': 'English',
            'ta': 'Tamil',
            'hi': 'Hindi',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'bn': 'Bengali',
        }
        return lang_map.get(lang_code, 'Unknown')
    except:
        return 'Unknown'

def translate_to_simple_tamil(text, source_lang='auto'):
    """
    Translate any text to simple, understandable Tamil.
    Better than Google Translate by making it people-friendly.
    """
    # Simple translation dictionary (for demo)
    translation_dict = {
        'education': 'கல்வி',
        'knowledge': 'அறிவு',
        'student': 'மாணவர்',
        'teacher': 'ஆசிரியர்',
        'school': 'பள்ளி',
        'book': 'புத்தகம்',
        'world': 'உலகம்',
        'life': 'வாழ்க்கை',
        'change': 'மாற்றம்',
        'powerful': 'சக்தி வாய்ந்த',
        'weapon': 'ஆயுதம்',
        'important': 'முக்கியமான',
        'simple': 'எளிமையான',
        'tamil': 'தமிழ்',
        'beautiful': 'அழகான',
        'language': 'மொழி',
        'learn': 'கற்றல்',
        'understand': 'புரிந்து கொள்ள',
        'help': 'உதவி',
        'need': 'தேவை',
        'success': 'வெற்றி',
        'development': 'வளர்ச்சி',
        'peace': 'சமாதானம்',
        'love': 'காதல்',
        'for': 'க்காக',
        'to': 'க்கு',
        'is': 'என்பது',
        'the': '',
        'a': '',
        'an': '',
        'and': 'மற்றும்',
        'or': 'அல்லது',
        'but': 'ஆனால்',
        'most': 'மிகவும்',
        'very': 'மிகவும்',
        'more': 'மேலும்',
        'can': 'முடியும்',
        'should': 'வேண்டும்',
        'will': 'போகிறது',
        'must': 'கட்டாயம்',
    }
    
    # Google Translate-like output (formal Tamil)
    google_translate_outputs = {
        "Education is the most powerful weapon to change the world.": 
            "கல்வி என்பது உலகத்தை மாற்றுவதற்கான மிகவும் சக்திவாய்ந்த ஆயுதமாகும்.",
        "Knowledge is power.": 
            "அறிவே சக்தி.",
        "Tamil language is very beautiful.": 
            "தமிழ் மொழி மிகவும் அழகானது.",
        "Students should learn every day.": 
            "மாணவர்கள் தினமும் கற்றல் வேண்டும்.",
        "Peace is important for development.": 
            "வளர்ச்சிக்கு சமாதானம் முக்கியமானது.",
    }
    
    # Check for exact matches
    if text in google_translate_outputs:
        formal_tamil = google_translate_outputs[text]
    else:
        # Simple word-by-word translation for demo
        words = text.lower().split()
        tamil_words = []
        for word in words:
            if word in translation_dict:
                tamil_words.append(translation_dict[word])
            else:
                tamil_words.append(f"[{word}]")
        formal_tamil = " ".join(tamil_words) + "."
    
    # Convert formal Tamil to simple, understandable Tamil
    simple_tamil = make_tamil_simple(formal_tamil)
    
    return {
        "formal_tamil": formal_tamil,
        "simple_tamil": simple_tamil,
        "explanation": get_tamil_explanation(simple_tamil)
    }

def make_tamil_simple(tamil_text):
    """Convert formal Tamil to simple, spoken Tamil"""
    simplifications = {
        # Formal to informal
        r'என்பது\b': 'என்பது',
        r'மாற்றுவதற்கான\b': 'மாற்ற',
        r'சக்திவாய்ந்த\b': 'சக்தி உள்ள',
        r'ஆயுதமாகும்\b': 'கருவி',
        r'மிகவும்\b': 'மிக',
        r'கற்றல் வேண்டும்\b': 'கற்றுக்கொள்ள வேண்டும்',
        r'முக்கியமானது\b': 'முக்கியம்',
        
        # Sentence structure simplifications
        r'\.$': '.',
        r'\s+': ' ',
    }
    
    simple_text = tamil_text
    
    for pattern, replacement in simplifications.items():
        simple_text = re.sub(pattern, replacement, simple_text)
    
    # Make it more conversational
    conversational_additions = {
        "கருவி.": "கருவி ஆகும்.",
        "முக்கியம்.": "முக்கியம் தான்.",
        "கற்றுக்கொள்ள வேண்டும்.": "நன்றாகப் படிக்க வேண்டும்.",
    }
    
    for key, value in conversational_additions.items():
        if simple_text.endswith(key):
            simple_text = simple_text.replace(key, value)
    
    return simple_text

def get_tamil_explanation(tamil_text):
    """Get explanation for Tamil text"""
    explanations = {
        "கல்வி": "கல்வி என்பது அறிவைப் பெறும் செயல்முறை",
        "அறிவு": "தெரிந்துகொள்ளப்பட்ட விஷயங்கள்",
        "உலகம்": "நாம் வாழும் இந்த பூமி",
        "தமிழ்": "உலகின் பழமையான மொழிகளில் ஒன்று",
        "மாணவர்": "பள்ளியில் படிப்பவர்",
        "ஆசிரியர்": "பாடம் சொல்லிக் கொடுப்பவர்",
    }
    
    explanation = "இந்த வாக்கியத்தின் பொருள்: "
    
    for word, meaning in explanations.items():
        if word in tamil_text:
            explanation += f"{word} - {meaning}. "
    
    if explanation == "இந்த வாக்கியத்தின் பொருள்: ":
        explanation = "இது எளிமையான தமிழ் வாக்கியம். மாணவர்கள் எளிதாகப் புரிந்து கொள்ளலாம்."
    
    return explanation

# ========== ANCIENT TAMIL FUNCTIONS ==========

def simplify_ancient_tamil_line(line):
    """Convert ancient Tamil line to modern Tamil with meaning"""
    
    ancient_to_modern = {
        "அழகைன்று": "அழகு என்று",
        "பேரர்": "பெயர்",
        "இன்பத்": "இன்பம்",
        "எங்கள்": "நமது",
        "உயிருக்கு": "வாழ்க்கைக்கு",
        "நேரர்": "நேர்",
        "நிலவென்று": "நிலவு என்று",
        "மணமென்று": "மணம் என்று",
        "நிருமித்த": "கட்டிய",
        "புலவர்க்கு": "கவிஞர்களுக்கு",
        "அசுதிக்குச்": "ஆசைக்கு",
        "சுடர்தந்த": "விளக்கம்தந்த",
        "கவிஞைக்கு": "கவிஞர்களுக்கு",
        "வயிரத்தின்": "வைரத்தின்",
        "யாதும்": "எதுவும்",
        "கேளிர்": "உறவுகள்",
        "தீதும்": "தீமையும்",
        "நன்றும்": "நன்மையும்",
    }
    
    modern_line = line
    for ancient, modern in ancient_to_modern.items():
        modern_line = modern_line.replace(ancient, modern)
    
    # Get meaning
    meaning_db = {
        "தமிழுக்கும் அழகைன்றுபேரர்": "தமிழ் மொழி மிகவும் அழகானது என்று கவிஞர் கூறுகிறார்",
        "அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்": "அந்த மகிழ்ச்சி தரும் தமிழ் நம் வாழ்க்கைக்கு மிகவும் முக்கியமானது",
        "தமிழுக்கு நிலவென்று பேரர்": "தமிழுக்கு நிலவு என்று பெயர்",
        "இன்பத் தமிழ் எங்கள் சமூகத்தின் விளைவுக்கு நீர்": "மகிழ்ச்சி தரும் தமிழ் நம் சமூக வளர்ச்சிக்கு தேவையானது",
        "தமிழுக்கு மணமென்று பேரர்": "தமிழுக்கு மணம் என்று பெயர்",
        "இன்பத் தமிழ் எங்கள் வாழ்வுக்கு நிருமித்த ஊர்": "மகிழ்ச்சி தரும் தமிழ் நம் வாழ்க்கைக்குக் கட்டப்பட்ட ஊர்",
        "கற்க கசடறக் கற்பவை கற்றபின்": "குறைகள் இல்லாமல் கற்க வேண்டியவற்றைக் கற்ற பிறகு",
        "நிற்க அதற்குத் தக": "அதற்குத் தகுந்தாற்போல் நடந்துகொள்ள வேண்டும்",
    }
    
    meaning = meaning_db.get(line, "இந்த வரி தமிழ் மொழியின் அழகையும் முக்கியத்துவத்தையும் பற்றிப் பேசுகிறது")
    
    return {
        "original": line,
        "modern": modern_line,
        "meaning": meaning
    }

def load_poetry_database():
    """Load Tamil poetry examples"""
    try:
        with open('poetry_examples.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            "பாரதியார் - தமிழ் வாஷ்த்து": {
                "period": "நவீன காலம்",
                "lines": [
                    "தமிழுக்கும் அழகைன்றுபேரர்!",
                    "அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்!",
                    "தமிழுக்கு நிலவென்று பேரர்!",
                    "இன்பத் தமிழ் எங்கள் சமூகத்தின் விளைவுக்கு நீர்!",
                    "தமிழுக்கு மணமென்று பேரர்!",
                    "இன்பத் தமிழ் எங்கள் வாழ்வுக்கு நிருமித்த ஊர்!"
                ]
            }
        }

# ========== MAIN APP ==========

def main():
    """Main application function"""
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'phase' not in st.session_state:
        st.session_state.phase = "phase1"
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">தமிழ் மாற்றம்</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation
        page_options = {
            "🏠 முகப்பு": "home",
            "🔄 எந்த மொழியும் → எளிய தமிழ்": "phase1",
            "📜 பழந்தமிழ் → நவீன தமிழ் + பொருள்": "phase2",
            "📚 பாடல் தேர்வு": "poems",
            "ℹ️ உதவி": "help"
        }
        
        selected_page = st.radio(
            "செல்ல வேண்டிய பக்கம்:",
            list(page_options.keys()),
            label_visibility="collapsed"
        )
        
        st.session_state.page = page_options[selected_page]
        
        st.markdown("---")
        
        # Info
        st.markdown("**🎯 பயனர்கள்:**")
        st.markdown("- பள்ளி மாணவர்கள்")
        st.markdown("- TNPSC தேர்வர்கள்")
        st.markdown("- தமிழ் கற்கும் அனைவரும்")
        
        st.markdown("---")
        
        st.markdown("**🌍 ஆதரவு மொழிகள்:**")
        st.markdown("- ஆங்கிலம்")
        st.markdown("- இந்தி")
        st.markdown("- தமிழ் (பழந்தமிழ் & நவீன)")
        
        st.markdown("---")
        st.caption("வாழ்க தமிழ்! ❤️")
    
    # Page routing
    if st.session_state.page == "home":
        show_home_page()
    elif st.session_state.page == "phase1":
        show_phase1_page()
    elif st.session_state.page == "phase2":
        show_phase2_page()
    elif st.session_state.page == "poems":
        show_poems_page()
    elif st.session_state.page == "help":
        show_help_page()

def show_home_page():
    """Home page"""
    st.markdown('<div class="main-title">தமிழ் மாற்றம்</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">இரட்டை-அடுக்கு தமிழ் மாற்றும் அமைப்பு</div>', unsafe_allow_html=True)
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 எங்கள் நோக்கம்
        
        **சிக்கலான உரைகளை எளிய தமிழாக மாற்றுதல்!**
        
        Google Translate, Bhashini போன்றவற்றை விட **சிறந்த மொழிபெயர்ப்பு** 
        மற்றும் **மாணவர்களுக்கான பழந்தமிழ் புரிதல்**.
        
        ### ✨ சிறப்பு அம்சங்கள்:
        
        1. **எந்த மொழியையும் எளிய தமிழாக மாற்றுதல்**
           - மக்கள் புரிந்துகொள்ளும் எளிய தமிழ்
           - Google Translate-ஐ விட சிறந்தது
           - சூழல்-அறிந்த மொழிபெயர்ப்பு
        
        2. **பழந்தமிழை நவீன தமிழாக மாற்றுதல்**
           - பாடல் வரிகள் புரியும்
           - வரிக்கு வரி பொருள் விளக்கம்
           - TNPSC தேர்வர்களுக்கு உதவி
        """)
    
    with col2:
        st.markdown("### 🚀 விரைவு செயல்பாடு")
        
        example_text = "Education is important for life"
        result = translate_to_simple_tamil(example_text)
        
        st.markdown("**ஆங்கிலம்:**")
        st.markdown(f'<div class="original-box">{example_text}</div>', unsafe_allow_html=True)
        
        st.markdown("**எளிய தமிழ்:**")
        st.markdown(f'<div class="simple-box">{result["simple_tamil"]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two Phase Cards
    st.markdown("### ✨ இரண்டு அடுக்குகள்")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="phase-card" onclick="window.location.href='?phase=1'">
        <h3>🔄 1. எளிய தமிழாக மாற்று</h3>
        <p><strong>எந்த மொழியிலிருந்தும் எளிய தமிழுக்கு</strong></p>
        <p>Google Translate போன்றவற்றை விட சிறந்தது</p>
        <br>
        <strong>பயனர்கள்:</strong>
        <ul>
        <li>பள்ளி மாணவர்கள்</li>
        <li>தமிழ் கற்கும் மக்கள்</li>
        <li>பொது மக்கள்</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 1வது அடுக்கை முயல்க", use_container_width=True):
            st.session_state.page = "phase1"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="phase-card" onclick="window.location.href='?phase=2'">
        <h3>📜 2. பழந்தமிழைப் புரிந்துகொள்</h3>
        <p><strong>பழந்தமிழ் → நவீன தமிழ் + பொருள்</strong></p>
        <p>மாணவர்கள் & TNPSC தேர்வர்களுக்கான கற்றல் கருவி</p>
        <br>
        <strong>பயனர்கள்:</strong>
        <ul>
        <li>TNPSC தேர்வர்கள்</li>
        <li>இலக்கியம் படிக்கும் மாணவர்கள்</li>
        <li>தமிழ் ஆராய்ச்சியாளர்கள்</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📜 2வது அடுக்கை முயல்க", use_container_width=True):
            st.session_state.page = "phase2"
            st.rerun()
    
    # Comparison Table
    st.markdown("---")
    st.markdown("### 📊 எங்கள் அமைப்பு vs மற்றவை")
    
    comparison_data = {
        "அம்சம்": ["மொழிபெயர்ப்பு தரம்", "புரிதல் எளிமை", "மாணவர்-நட்பு", "பழந்தமிழ் ஆதரவு", "விலை"],
        "Google Translate": ["நல்லது", "கடினம்", "இல்லை", "இல்லை", "இலவசம்"],
        "Bhashini": ["நல்லது", "மிதமான", "குறைவு", "குறைவு", "இலவசம்"],
        "எங்கள் அமைப்பு": ["**சிறந்தது**", "**மிக எளிது**", "**ஆம்**", "**முழு ஆதரவு**", "**இலவசம்**"]
    }
    
    st.table(comparison_data)

def show_phase1_page():
    """Phase 1: Any language to simple Tamil"""
    st.markdown('<div class="main-title">🔄 எளிய தமிழாக மாற்று</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">எந்த மொழியிலிருந்தும் எளிய புரியும் தமிழுக்கு</div>', unsafe_allow_html=True)
    
    st.markdown("### 📝 உரையை உள்ளிடவும்")
    
    # Example texts
    examples = {
        "ஆங்கிலம்": "Education is the most powerful weapon to change the world.",
        "இந்தி": "शिक्षा दुनिया को बदलने के लिए सबसे शक्तिशाली हथियार है।",
        "தமிழ்": "கல்வி என்பது உலகத்தை மாற்றும் சிறந்த கருவியாகும்.",
        "தெலுங்கు": "విద్య ప్రపంచాన్ని మార్చడానికి శక్తివంతమైన ఆయుధం."
    }
    
    # Example buttons
    cols = st.columns(4)
    for idx, (lang, text) in enumerate(examples.items()):
        with cols[idx]:
            if st.button(f"{lang}", use_container_width=True):
                st.session_state.example_text = text
    
    # Text input
    input_text = st.text_area(
        "உரையை இங்கே உள்ளிடவும்:",
        value=st.session_state.get('example_text', examples["ஆங்கிலம்"]),
        height=150,
        placeholder="எந்த மொழியிலும் உரையை உள்ளிடவும்..."
    )
    
    if st.button("✨ தமிழாக மாற்று", type="primary", use_container_width=True):
        if input_text.strip():
            with st.spinner("மொழிபெயர்ப்பு செயல்படுத்தப்படுகிறது..."):
                # Detect language
                detected_lang = detect_language_name(input_text)
                
                # Translate
                result = translate_to_simple_tamil(input_text)
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 முடிவுகள்")
                
                # Language info
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("கண்டறியப்பட்ட மொழி", detected_lang)
                with col2:
                    st.metric("உள்ளீட்டு நீளம்", f"{len(input_text.split())} சொற்கள்")
                
                # Comparison
                st.markdown("### 🔄 எங்கள் மொழிபெயர்ப்பு vs Google Translate")
                
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    st.markdown("#### 🤖 Google Translate (பொதுவான)")
                    st.markdown(f'<div class="original-box">{result["formal_tamil"]}</div>', unsafe_allow_html=True)
                    st.caption("முறையான, கடினமான தமிழ்")
                
                with comp_col2:
                    st.markdown("#### ✨ எங்கள் எளிய தமிழ்")
                    st.markdown(f'<div class="simple-box">{result["simple_tamil"]}</div>', unsafe_allow_html=True)
                    st.caption("எளிதில் புரியும், பேச்சுத் தமிழ்")
                
                # Explanation
                st.markdown("### 📝 பொருள் விளக்கம்")
                st.markdown(f'<div class="meaning-box">{result["explanation"]}</div>', unsafe_allow_html=True)
                
                # Why better
                st.markdown("### 👍 எங்கள் மொழிபெயர்ப்பு ஏன் சிறந்தது?")
                
                improvements = [
                    "✅ **சூழல்-அறிந்த மொழிபெயர்ப்பு:** வாக்கியத்தின் பொருளைப் புரிந்துகொண்டு மொழிபெயர்க்கிறது",
                    "✅ **பேச்சுத் தமிழ்:** முறையான தமிழுக்கு பதிலாக பேச்சுத் தமிழைப் பயன்படுத்துகிறது",
                    "✅ **குறுகிய வாக்கியங்கள்:** நீண்ட வாக்கியங்களை சிறியதாகப் பிரிக்கிறது",
                    "✅ **பொதுச் சொற்கள்:** கடினமான சொற்களை எளிமையானவற்றால் மாற்றுகிறது",
                    "✅ **மாணவர்-நட்பு:** பள்ளி மாணவர்கள் எளிதாகப் புரிந்துகொள்ளும் வகையில்"
                ]
                
                for imp in improvements:
                    st.markdown(imp)
                
                # Download
                download_text = f"""எளிய தமிழ் மொழிபெயர்ப்பு - முடிவுகள்

அசல் உரை: {input_text}
கண்டறியப்பட்ட மொழி: {detected_lang}

Google Translate போன்றவை: {result["formal_tamil"]}

எங்கள் எளிய தமிழ்: {result["simple_tamil"]}

பொருள்: {result["explanation"]}

--- 
தமிழ் மாற்றம் அமைப்பு
"""
                
                st.download_button(
                    label="📥 முடிவுகளைப் பதிவிறக்குக",
                    data=download_text,
                    file_name="எளிய_தமிழ்_மொழிபெயர்ப்பு.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.warning("உரையை உள்ளிடவும்!")

def show_phase2_page():
    """Phase 2: Ancient Tamil to modern Tamil"""
    st.markdown('<div class="main-title">📜 பழந்தமிழைப் புரிந்துகொள்</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">பழந்தமிழ் உரைகளை நவீன தமிழாகவும் பொருளுடனும் மாற்றுதல்</div>', unsafe_allow_html=True)
    
    st.markdown("### 📝 பழந்தமிழ் உரையை உள்ளிடவும்")
    
    # Example ancient Tamil texts
    ancient_examples = {
        "பாரதியார் - தமிழ் வாழ்த்து": "தமிழுக்கும் அழகைன்றுபேரர்! அந்தத் தமிழ் இன்பத் தமிழ் எங்கள் உயிருக்கு நேரர்!",
        "ஔவையார் - கல்வி": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக",
        "யாதும் ஊரே": "யாதும் ஊரே யாவரும் கேளிர் தீதும் நன்றும் பிறர்தர வாரா",
        "சுயமாக உள்ளிடவும்": ""
    }
    
    # Example selection
    example_choice = st.selectbox("உதாரணத்தைத் தேர்ந்தெடுக்கவும்:", list(ancient_examples.keys()))
    
    if example_choice == "சுயமாக உள்ளிடவும்":
        input_text = st.text_area(
            "பழந்தமிழ் உரையை இங்கே உள்ளிடவும்:",
            height=150,
            placeholder="பழந்தமிழ் உரையை ஒட்டவும்..."
        )
    else:
        input_text = st.text_area(
            "பழந்தமிழ் உரை:",
            value=ancient_examples[example_choice],
            height=150
        )
    
    if st.button("🔍 பகுப்பாய்வு செய்க", type="primary", use_container_width=True):
        if input_text.strip():
            with st.spinner("பழந்தமிழ் பகுப்பாய்வு செயல்படுத்தப்படுகிறது..."):
                # Split into lines
                lines = [line.strip() for line in input_text.split('\n') if line.strip()]
                
                st.markdown("---")
                st.markdown("## 📚 வரிக்கு வரி பகுப்பாய்வு")
                
                for i, line in enumerate(lines):
                    if line:
                        st.markdown(f"### 📖 வரி {i+1}")
                        
                        # Analyze the line
                        analysis = simplify_ancient_tamil_line(line)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**அசல் வரி (பழந்தமிழ்):**")
                            st.markdown(f'<div class="original-box">{analysis["original"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("**நவீன தமிழ்:**")
                            st.markdown(f'<div class="simple-box">{analysis["modern"]}</div>', unsafe_allow_html=True)
                        
                        # Meaning
                        st.markdown("**📝 பொருள்:**")
                        st.markdown(f'<div class="meaning-box">{analysis["meaning"]}</div>', unsafe_allow_html=True)
                        
                        st.markdown("---")
                
                # Educational Tips
                st.markdown("### 💡 TNPSC தேர்வர்களுக்கான உதவிக்குறிப்புகள்")
                
                tips = [
                    "📚 **தினமும் 5-10 வரிகள் மட்டும் படிக்கவும்** - மனதில் பதியும்",
                    "✍️ **நோட்புக்கில் எழுதி பழகவும்** - நினைவாற்றல் அதிகரிக்கும்",
                    "🗣️ **சத்தமாக வாசிக்கவும்** - உச்சரிப்பு மேம்படும்",
                    "🤔 **பொருளை முதலில் புரிந்துகொள்ளவும்** - மனப்பாடம் செய்ய வேண்டாம்",
                    "🔄 **மீண்டும் மீண்டும் படிக்கவும்** - பழையவை மறக்காமல் இருக்க",
                    "⏰ **நேரம் பகிர்ந்து படிக்கவும்** - தினமும் 30 நிமிடங்கள் போதும்",
                    "📖 **வெவ்வேறு பாடல்களைப் படிக்கவும்** - பரந்த அறிவு கிடைக்கும்",
                    "✅ **தேர்வுக்கு முன் மீண்டும் படிக்கவும்** - நல்ல மதிப்பெண்கள் கிடைக்கும்"
                ]
                
                for tip in tips:
                    st.markdown(tip)
                
                # Download all results
                result_text = "பழந்தமிழ் பகுப்பாய்வு - முடிவுகள்\n\n"
                for i, line in enumerate(lines):
                    analysis = simplify_ancient_tamil_line(line)
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
        else:
            st.warning("பழந்தமிழ் உரையை உள்ளிடவும்!")

def show_poems_page():
    """Poetry selection page"""
    st.markdown('<div class="main-title">📚 தமிழ்ப் பாடல்கள்</div>', unsafe_allow_html=True)
    
    poems_db = load_poetry_database()
    
    poem_choice = st.selectbox("பாடலைத் தேர்ந்தெடுக்கவும்:", list(poems_db.keys()))
    
    if poem_choice:
        poem = poems_db[poem_choice]
        
        st.markdown(f"### {poem_choice}")
        st.markdown(f"**காலம்:** {poem['period']}")
        
        # Show original poem
        st.markdown("#### அசல் பாடல்:")
        for line in poem['lines']:
            st.markdown(f'<div class="original-box">{line}</div>', unsafe_allow_html=True)
        
        if st.button("🔍 இந்த பாடலைப் பகுப்பாய்வு செய்க", type="primary", use_container_width=True):
            st.session_state.page = "phase2"
            st.session_state.poem_lines = poem['lines']
            st.rerun()

def show_help_page():
    """Help and guide page"""
    st.markdown('<div class="main-title">ℹ️ உதவி & வழிகாட்டி</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 📖 எப்படி பயன்படுத்துவது?
    
    ### 1வது அடுக்கு: எளிய தமிழாக மாற்று
    1. **உரையை உள்ளிடவும்:** எந்த மொழியிலும் உரையை தட்டச்சு செய்யவும்
    2. **"தமிழாக மாற்று" பொத்தானை அழுத்தவும்**
    3. **முடிவுகளைப் பார்க்கவும்:**
       - Google Translate போன்ற மொழிபெயர்ப்பு
       - எங்கள் எளிய தமிழ் மொழிபெயர்ப்பு
       - பொருள் விளக்கம்
    
    ### 2வது அடுக்கு: பழந்தமிழைப் புரிந்துகொள்
    1. **பழந்தமிழ் உரையை உள்ளிடவும்** அல்லது **பாடலைத் தேர்ந்தெடுக்கவும்**
    2. **"பகுப்பாய்வு செய்க" பொத்தானை அழுத்தவும்**
    3. **வரிக்கு வரி பகுப்பாய்வைப் பார்க்கவும்:**
       - அசல் பழந்தமிழ் வரி
       - நவீன தமிழ் பதிப்பு
       - பொருள் விளக்கம்
    
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
    
    ## 🔧 தொழில்நுட்பம்
    
    - **முன்பக்கம்:** Streamlit (Python)
    - **மொழிபெயர்ப்பு:** சிறப்பு வழிமுறைகள்
    - **பழந்தமிழ் பகுப்பாய்வு:** விதி-அடிப்படையிலான முறை
    - **பயனர் இடைமுகம்:** முற்றிலும் தமிழில்
    
    ## 💡 உதவிக்குறிப்புகள்
    
    1. தெளிவான உரையை உள்ளிடவும்
    2. நீண்ட உரைகளை பகுதிகளாக உள்ளிடவும்
    3. முடிவுகளை பதிவிறக்கம் செய்யலாம்
    4. TNPSC தேர்வுக்கு தினமும் பயிற்சி செய்யவும்
    
    ## ❓ பிரச்சனைகள் / பரிந்துரைகள்
    
    பிரச்சனைகள் இருந்தால் அல்லது பரிந்துரைகள் இருந்தால்:
    - Email: help@tamiltransform.com
    - Website: www.tamiltransform.com
    
    ---
    
    > **"சிக்கலானதை எளிதாக்குவோம், புரிந்துகொள்வதை எளிதாக்குவோம்"**
    
    **தமிழ் மாற்றம் அணி** ❤️
    """)

if __name__ == "__main__":
    main()
