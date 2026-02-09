import streamlit as st
import pandas as pd
import json
import re

# Page config
st.set_page_config(
    page_title="Arivu-Tamil",
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
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
}
.stButton > button {
    background-color: #2E86AB;
    color: white;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #1B4F72;
}
</style>
""", unsafe_allow_html=True)

# SIMPLE TRANSLATION DICTIONARY (No external API needed)
TRANSLATION_DICT = {
    # Common English to Tamil
    'education': 'கல்வி',
    'knowledge': 'அறிவு',
    'student': 'மாணவர்',
    'teacher': 'ஆசிரியர்',
    'school': 'பள்ளி',
    'learn': 'கற்றல்',
    'book': 'புத்தகம்',
    'world': 'உலகம்',
    'life': 'வாழ்க்கை',
    'change': 'மாற்றம்',
    'powerful': 'சக்தி வாய்ந்த',
    'weapon': 'ஆயுதம்',
    'important': 'முக்கியமான',
    'simple': 'எளிமையான',
    'complex': 'சிக்கலான',
    'understand': 'புரிந்து கொள்ள',
    'language': 'மொழி',
    'tamil': 'தமிழ்',
    'beautiful': 'அழகான',
    'good': 'நல்ல',
    'great': 'பெரிய',
    'small': 'சிறிய',
    'big': 'பெரிய',
    'help': 'உதவி',
    'need': 'தேவை',
    'want': 'விரும்பு',
    'love': 'காதல்',
    'peace': 'சமாதானம்',
    
    # Phrases
    'is the': 'என்பது',
    'to change': 'மாற்றுவதற்கு',
    'for life': 'வாழ்க்கைக்காக',
    'most powerful': 'மிகவும் சக்தி வாய்ந்த',
}

# Tamil simplification rules
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
        'வான்': 'வானம்',
        'தோள்': 'தோள்கள்',
        'வாள்': 'வாள்',
        'பால்': 'பால்',
        'வேல்': 'ஆயுதம்',
        'தேன்': 'தேன்',
        'யாதும்': 'எதுவும்',
        'கேளிர்': 'உறவுகள்',
        'தீதும்': 'தீமையும்',
        'நன்றும்': 'நன்மையும்',
    }
    
    for old, new in simplifications.items():
        text = text.replace(old, new)
    
    return text

# Simple translation function
def translate_to_tamil(text):
    """Simple rule-based English to Tamil translation"""
    text_lower = text.lower()
    
    # Check for exact matches in dictionary
    for eng, tam in TRANSLATION_DICT.items():
        if eng in text_lower:
            # Replace the word
            pattern = re.compile(re.escape(eng), re.IGNORECASE)
            text = pattern.sub(tam, text)
    
    # If no translation found, return with marker
    if text == text_lower:
        return text + " [மொழிபெயர்ப்பு தேவை]"
    
    return text

# Load poetry examples
def load_poems():
    """Load Tamil poems from JSON or return default"""
    try:
        with open('poetry_examples.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
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
            },
            "கல்வி": {
                "author": "ஔவையார்", 
                "period": "Classical",
                "lines": [
                    "கற்க கசடறக் கற்பவை கற்றபின்",
                    "நிற்க அதற்குத் தக"
                ]
            }
        }

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("# 📚 அறிவு-தமிழ்")
        st.markdown("---")
        st.markdown("### Navigate")
        page = st.radio("Choose a page:", 
                       ["🏠 Home", "🔄 Text Simplifier", "📜 Poetry Explainer", "ℹ️ About"])
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("- Text simplification")
        st.markdown("- Poetry analysis")
        st.markdown("- Student-friendly")
        st.markdown("---")
        st.caption("Made for Tamil learners")
    
    # Page content
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔄 Text Simplifier":
        show_simplifier_page()
    elif page == "📜 Poetry Explainer":
        show_poetry_page()
    elif page == "ℹ️ About":
        show_about_page()

def show_home_page():
    st.markdown('<div class="main-header">அறிவு-தமிழ்</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:1.2rem; color:#5D5D5D;">AI-Powered Tamil Simplification System</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Our Mission")
        st.markdown("""
        To make Tamil literature and complex texts 
        **accessible to everyone** through intelligent 
        simplification and explanation.
        
        **Perfect for:**
        - School students
        - Tamil learners  
        - Competitive exams
        - Slow learners
        """)
        
        if st.button("Try Text Simplifier →", use_container_width=True):
            st.session_state.page = "simplifier"
    
    with col2:
        st.markdown("### 🚀 Quick Demo")
        demo_text = st.text_area(
            "Try it now:",
            "Education is important for life",
            height=100
        )
        
        if st.button("Simplify This", use_container_width=True):
            tamil_text = translate_to_tamil(demo_text)
            simple_text = simplify_tamil(tamil_text)
            
            st.markdown("**Result:**")
            st.markdown(f'<div class="simple-text">{simple_text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Key Features")
    
    features = {
        "📝 Text Simplifier": "Convert any text to simple Tamil",
        "📜 Poetry Explainer": "Understand Tamil poems line-by-line", 
        "🎯 Student Focus": "Designed for easy learning",
        "🚀 Instant Results": "No waiting, immediate output"
    }
    
    cols = st.columns(4)
    for (feature, desc), col in zip(features.items(), cols):
        with col:
            st.markdown(f"**{feature}**")
            st.markdown(f"<small>{desc}</small>", unsafe_allow_html=True)

def show_simplifier_page():
    st.markdown('<div class="main-header">🔄 Text Simplifier</div>', unsafe_allow_html=True)
    
    # Input options
    input_method = st.radio(
        "Choose input type:",
        ["📝 Text Input", "📄 Example Texts"],
        horizontal=True
    )
    
    if input_method == "📝 Text Input":
        input_text = st.text_area(
            "Enter text to simplify (English or Tamil):",
            height=150,
            placeholder="Type or paste your text here...",
            help="You can enter English or Tamil text. The system will translate and simplify it."
        )
        
        examples = st.columns(3)
        with examples[0]:
            if st.button("Education Example", use_container_width=True):
                st.session_state.demo_text = "Education is the most powerful weapon to change the world."
        with examples[1]:
            if st.button("Knowledge Example", use_container_width=True):
                st.session_state.demo_text = "Knowledge gives power to understand the world."
        with examples[2]:
            if st.button("Tamil Example", use_container_width=True):
                st.session_state.demo_text = "தமிழ் மொழி மிகவும் அழகானது"
        
        if 'demo_text' in st.session_state:
            input_text = st.text_area("Enter text:", st.session_state.demo_text, height=150)
    
    else:  # Example Texts
        example_choice = st.selectbox(
            "Choose an example:",
            [
                "Education is important for success",
                "Tamil language is very beautiful", 
                "Learning new things is good for brain",
                "Books are best friends",
                "Peace is needed for development"
            ]
        )
        input_text = example_choice
    
    if input_text and st.button("✨ Simplify Text", type="primary", use_container_width=True):
        with st.spinner("Processing..."):
            # Translate to Tamil if needed
            if any(ord(c) > 127 for c in input_text):  # Check if already Tamil
                tamil_text = input_text
            else:
                tamil_text = translate_to_tamil(input_text)
            
            # Simplify Tamil text
            simplified_text = simplify_tamil(tamil_text)
            
            # Display results
            st.markdown("---")
            st.markdown("## 📊 Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📖 Tamil Version")
                st.markdown(f'<div class="tamil-text">{tamil_text}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### ✨ Simplified Tamil")
                st.markdown(f'<div class="simple-text">{simplified_text}</div>', unsafe_allow_html=True)
            
            # Explanation
            st.markdown("### 📝 Explanation")
            if "கல்வி" in tamil_text:
                st.info("""
                **கல்வி** என்பது மனித வாழ்க்கையை முழுமையாக மாற்றக்கூடிய சக்தி வாய்ந்த கருவியாகும். 
                கல்வி மூலம் நாம் உலகத்தை நன்கு புரிந்து கொள்ள முடியும்.
                """)
            elif "தமிழ்" in tamil_text:
                st.info("""
                **தமிழ் மொழி** உலகின் பழமையான மொழிகளில் ஒன்றாகும். 
                இது இலக்கியம், கவிதை, இசை ஆகிய துறைகளில் மிகுந்த செழுமை கொண்டது.
                """)
            else:
                st.info("இந்த வாக்கியம் எளிமையான தமிழில் விளக்கப்பட்டுள்ளது.")
            
            # Download button
            st.download_button(
                label="📥 Download Simplified Text",
                data=simplified_text,
                file_name="simplified_tamil.txt",
                mime="text/plain",
                use_container_width=True
            )

def show_poetry_page():
    st.markdown('<div class="main-header">📜 Poetry Explainer</div>', unsafe_allow_html=True)
    
    # Load poems
    poems = load_poems()
    
    # Poem selection
    poem_choice = st.selectbox(
        "Choose a Tamil poem:",
        list(poems.keys())
    )
    
    if poem_choice:
        poem = poems[poem_choice]
        
        st.markdown(f"### {poem_choice}")
        st.markdown(f"**Author:** {poem['author']} | **Period:** {poem['period']}")
        
        if 'explanation' in poem:
            st.info(poem['explanation'])
        
        st.markdown("---")
        st.markdown("### 📖 Original Poem")
        
        for i, line in enumerate(poem['lines']):
            st.markdown(f'<div class="tamil-text">{i+1}. {line}</div>', unsafe_allow_html=True)
        
        if st.button("🔍 Analyze This Poem", type="primary", use_container_width=True):
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
                
                # Meaning
                with st.expander("📝 Meaning & Explanation"):
                    if "தமிழ்" in line and "அழகு" in line:
                        st.markdown("""
                        **Meaning:** "Tamil has the name 'beauty'" - The poet says Tamil language is very beautiful.
                        
                        **Explanation:** The poet praises the aesthetic quality of Tamil language, 
                        comparing it to beauty itself. This is a metaphorical way of expressing 
                        the elegance and richness of the language.
                        """)
                    elif "இன்பத்" in line:
                        st.markdown("""
                        **Meaning:** "Happy/pleasant Tamil is water for our society's growth"
                        
                        **Explanation:** The poet compares pleasant Tamil language to water, 
                        which is essential for growth. Just as plants need water to grow, 
                        society needs beautiful language to develop culturally.
                        """)
                    else:
                        st.markdown(f"""
                        **General Meaning:** This line praises the Tamil language.
                        
                        **Key Words:**
                        - தமிழ்: Tamil language
                        - எங்கள்: Our
                        - உயிரு: Life
                        
                        The poet expresses deep connection with Tamil language.
                        """)
                
                st.markdown("---")

def show_about_page():
    st.markdown('<div class="main-header">ℹ️ About Arivu-Tamil</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 Project Overview
    
    **Arivu-Tamil** (அறிவு-தமிழ்) is an intelligent system designed to make Tamil literature 
    and complex texts accessible to students and learners through simplification.
    
    ### 🚀 Why We Built This
    
    Students often struggle with:
    - Complex literary Tamil
    - Archaic words and phrases  
    - Poetic metaphors
    - Cultural references
    
    Our system bridges this gap by providing **context-aware simplifications**.
    
    ### 🔧 Technology
    
    - **Frontend:** Streamlit (Python web framework)
    - **Translation:** Rule-based dictionary system
    - **Simplification:** Pattern matching and replacement
    - **Deployment:** Streamlit Cloud / Local
    
    ### 📊 Features
    
    1. **Text Simplifier**
       - Any text → Simple Tamil
       - Meaning-based translation
    
    2. **Poetry Explainer**  
       - Line-by-line analysis
       - Archaic word explanations
       - Poetic device identification
    
    ### 👥 Target Users
    
    - School students (Class 6-12)
    - Tamil language learners
    - Competitive exam aspirants
    - Teachers and educators
    
    ---
    
    ### 🏆 Our Vision
    
    > **"சிக்கலானதை எளிதாக்குவோம், புரிந்துகொள்வதை எளிதாக்குவோம்"**
    > 
    > *"Let's simplify complexity, make understanding easy"*
    
    ---
    
    **Note:** This is a demonstration version. The full system would include:
    - AI models for better translation
    - Larger Tamil database
    - Voice input/output
    - Mobile app version
    
    **Developed with ❤️ for Tamil learners**
    """)

if __name__ == "__main__":
    main()



