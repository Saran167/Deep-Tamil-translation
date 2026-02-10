import streamlit as st

st.set_page_config(
    page_title="Tamil Language Simplifier",
    page_icon="🪔",
    layout="centered"
)

st.title("Tamil Language Simplifier")
st.caption("Phase 1: Language → Simple Tamil | Phase 2: Archaeological Tamil → Simple Tamil")

source_type = st.selectbox(
    "Select input type",
    [
        "Modern / Mixed Language",
        "Archaeological / Ancient Tamil"
    ]
)

user_text = st.text_area(
    "Enter your text",
    height=160,
    placeholder="Paste text here..."
)

if st.button("Simplify"):
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        st.success("Base app is running correctly ✅")
        st.markdown("### Input Preview")
        st.write(user_text)
        st.markdown("### Selected Source")
        st.write(source_type)







