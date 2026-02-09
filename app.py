import streamlit as st
import pandas as pd
import json
from googletrans import Translator

# Page config
st.set_page_config(page_title="Arivu-Tamil", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
.tamil-text {font-size: 1.5rem; color: #D35400; font-family: 'Arial Unicode MS';}
.simple-text {font-size: 1.3rem; color: #27AE60; background: #F8F9F9; padding: 15px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Load Tamil data
def load_poems():
    with open('poetry_examples.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Tamil simplification rules
def simplify_tamil(text):
    simplifications = {
        'அழகைன்று': 'அழகு என்று',
        'பேரர்': 'பெயர்',
        'இன்பத்': 'இன்ப',
        'எங்கள்': 'நமது',
        'நேரர்': 'நேர்',
        'நிருமித்த': 'கட்டிய',
        'புலவர்க்கு': 'கவிஞர்களுக்கு',
        'அசுதிக்குச்': 'ஆசைக்கு',
    }
    for old, new in simplifications.items():
        text = text.replace(old, new)
    return text

# Translate function
def translate_to_tamil(text):
    translator = Translator()
    try:
        return translator.translate(text, dest='ta').text
    except:
        return text + " (Tamil translation)"

# Main app
def main():
    st.title("📚 அறிவு-தமிழ்")
    st.subheader("Tamil Simplification & Learning System")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Text Simplifier", "Poetry Explainer", "About"])
    
    with tab1:
        st.header("🔄 Text Simplifier")
        input_text = st.text_area("Enter text in any language:", 
                                 "Education is the most powerful weapon to change the world.",
                                 height=100)
        
        if st.button("Simplify to Tamil"):
            # Translate
            tamil_text = translate_to_tamil(input_text)
            # Simplify
            simple_tamil = simplify_tamil(tamil_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original Translation:**")
                st.markdown(f'<div class="tamil-text">{tamil_text}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Simplified Tamil:**")
                st.markdown(f'<div class="simple-text">{simple_tamil}</div>', unsafe_allow_html=True)
            
            # Explanation
            st.markdown("**Explanation:**")
            if "கல்வி" in tamil_text:
                st.info("கல்வி என்பது மனித வாழ்க்கையை மாற்றும் சக்தி வாய்ந்த கருவியாகும்.")
    
    with tab2:
        st.header("📜 Poetry Explainer")
        poems = load_poems()
        
        poem_choice = st.selectbox("Choose a poem:", list(poems.keys()))
        
        if poem_choice:
            poem = poems[poem_choice]
            st.markdown(f"**Author:** {poem['author']} | **Period:** {poem['period']}")
            
            for i, line in enumerate(poem['lines']):
                with st.expander(f"Line {i+1}: {line[:30]}..."):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original:**")
                        st.markdown(f'<div class="tamil-text">{line}</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown("**Simplified:**")
                        st.markdown(f'<div class="simple-text">{simplify_tamil(line)}</div>', unsafe_allow_html=True)
                    
                    st.markdown("**Meaning:**")
                    st.info("This line praises the beauty and importance of Tamil language.")
    
    with tab3:
        st.header("About")
        st.markdown("""
        ## Arivu-Tamil Project
        
        This system helps students understand complex Tamil texts through simplification.
        
        **Features:**
        - Text simplification from any language to simple Tamil
        - Tamil poetry line-by-line explanation
        - Educational focus for students
        
        **Technology:**
        - Python + Streamlit
        - Google Translate API
        - Rule-based Tamil simplification
        
        **Future Improvements:**
        - AI models for better simplification
        - More Tamil literature
        - Mobile app version
        """)

if __name__ == "__main__":
    main()




