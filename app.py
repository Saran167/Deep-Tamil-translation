import streamlit as st
import json
import re

# Page config
st.set_page_config(
    page_title="Arivu-Tamil",
    page_icon="📚", 
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E86AB;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: bold;
}
.tamil-text {
    font-size: 1.5rem;
    color: #D35400;
    font-family: 'Arial Unicode MS', sans-serif;
    line-height: 1.8;
    padding: 10px;
    background: #FFF3E0;
    border-radius: 8px;
    margin: 10px 0;
}
.simple-text {
    font-size: 1.3rem;
    color: #27AE60;
    font-family: 'Arial Unicode MS', sans-serif;
    line-height: 1.8;
    background-color: #E8F6F3;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #27AE60;
    margin: 10px 0;
}
.stButton > button {
    background-color: #2E86AB;
    color: white;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ========== SIMPLE TRANSLATION FUNCTIONS ==========

def translate_to_tamil(text):
    """Simple rule-based English to Tamil translation"""
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
    }
    
    words = text.lower().split()
    tamil_words = []
    
    for word in words:
        if word in translation_dict:
            tamil_words.append(translation_dict[word])
        else:
            tamil_words.append(word)
    
    return " ".join(tamil_words)

def simplify_tamil(text):
    """Simplify literary Tamil to modern Tamil"""
    simplifications = {
        'அழகைன்று': 'அழகு என்று',
        'பேரர்': 'பெயர்',
        'இன்பத்': 'இன்பம்',
        'எங்கள்': 'நமது',
        'உயிருக்கு': 'வாழ்க்கைக்கு',
        'நேரர்': 'நேர்',
        'நிலவென்று': 'நிலவு என்று',
        'மணமென்று': 'மணம் என்று',
        'நிருமித்த': 'கட்டிய',
        'புலவர்க்கு': 'கவிஞர்களுக்கு',
        'அசுதிக்குச்': 'ஆசைக்கு',
        'சுடர்தந்த': 'விளக்கம்தந்த',
        'கவிஞைக்கு': 'கவிஞர்களுக்கு',
        'வயிரத்தின்': 'வைரத்தின்',
    }
    
    for old, new in simplifications.items():
        text = text.replace(old, new)
    
    return text

# ========== LOAD POEMS ==========

def load_poems():
    """Load poems from JSON file"""
    try:
        with open('poetry_examples.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default poems if file not found
        return {
            "தமிழ் வாழ்த்து": {
                "author": "பாரதியார்",
                "period": "Modern",
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
    except json.JSONDecodeError as e:
        st.error(f"Error reading JSON file: {e}")
        return {}

# ========== MAIN APP ==========

def main():
    # Sidebar
    with st.sidebar:
        st.title("📚 அறிவு-தமிழ்")
        st.markdown("---")
        page = st.radio(
            "Choose Page:",
            ["🏠 Home", "🔄 Text Simplifier", "📜 Poetry Explainer"]
        )
    
    # Load poems once
    poems = load_poems()
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔄 Text Simplifier":
        show_simplifier_page()
    elif page == "📜 Poetry Explainer":
        show_poetry_page(poems)

def show_home_page():
    st.markdown('<div class="main-header">அறிவு-தமிழ்</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:1.2rem; color:#5D5D5D;">Tamil Simplification & Learning System</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Our Mission")
        st.markdown("""
        Make Tamil literature accessible:
        - Text simplification
        - Poetry explanation  
        - Student-friendly
        """)
    
    with col2:
        st.markdown("### 🚀 Quick Demo")
        demo_text = "Education is important for life"
        tamil_text = translate_to_tamil(demo_text)
        simple_text = simplify_tamil(tamil_text)
        
        st.markdown("**English:** " + demo_text)
        st.markdown("**Tamil:** " + tamil_text)
        st.markdown("**Simplified:**")
        st.markdown(f'<div class="simple-text">{simple_text}</div>', unsafe_allow_html=True)

def show_simplifier_page():
    st.markdown('<div class="main-header">🔄 Text Simplifier</div>', unsafe_allow_html=True)
    
    # Input
    input_text = st.text_area(
        "Enter text to simplify:",
        height=100,
        value="Education is important for life"
    )
    
    # Process
    if st.button("✨ Simplify Text", type="primary"):
        if input_text:
            # Check if input is already Tamil
            if any(ord(c) > 127 for c in input_text):
                tamil_text = input_text
            else:
                tamil_text = translate_to_tamil(input_text)
            
            simplified = simplify_tamil(tamil_text)
            
            # Display results
            st.markdown("## 📊 Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📖 Tamil Version")
                st.markdown(f'<div class="tamil-text">{tamil_text}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### ✨ Simplified Tamil")
                st.markdown(f'<div class="simple-text">{simplified}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter some text!")

def show_poetry_page(poems):
    st.markdown('<div class="main-header">📜 Poetry Explainer</div>', unsafe_allow_html=True)
    
    if not poems:
        st.error("No poems loaded. Check your JSON file.")
        return
    
    poem_choice = st.selectbox("Choose a poem:", list(poems.keys()))
    
    if poem_choice and poem_choice in poems:
        poem = poems[poem_choice]
        
        st.markdown(f"### {poem_choice}")
        st.markdown(f"**Author:** {poem['author']} | **Period:** {poem['period']}")
        
        # Show original poem
        st.markdown("#### Original Poem:")
        for line in poem['lines']:
            st.markdown(f'<div class="tamil-text">{line}</div>', unsafe_allow_html=True)
        
        if st.button("🔍 Analyze This Poem", type="primary"):
            st.markdown("---")
            st.markdown("## 📚 Line-by-Line Analysis")
            
            for i, line in enumerate(poem['lines']):
                st.markdown(f"### Line {i+1}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original:**")
                    st.markdown(f'<div class="tamil-text">{line}</div>', unsafe_allow_html=True)
                
                with col2:
                    simplified = simplify_tamil(line)
                    st.markdown("**Simplified:**")
                    st.markdown(f'<div class="simple-text">{simplified}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.warning("Select a poem from the list")

if __name__ == "__main__":
    main()

