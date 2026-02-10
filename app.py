import streamlit as st
from core.simplifier import simplify_modern_text

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Tamil Language Simplifier",
    page_icon="🪔",
    layout="centered"
)

# ------------------ Title ------------------
st.title("Tamil Language Simplifier")
st.caption(
    "Phase 1: Modern / Mixed Language → Simple Tamil | "
    "Phase 2: Archaeological / Ancient Tamil → Simple Tamil"
)

# ------------------ Input Selection ------------------
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

# ------------------ Action ------------------
if st.button("Simplify"):
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        # -------- Phase 1 --------
        if source_type == "Modern / Mixed Language":
            result = simplify_modern_text(user_text)

            st.subheader("Simple Tamil")
            st.write(result["simple_tamil"])

            st.subheader("People-Friendly Tamil")
            st.write(result["people_tamil"])

        # -------- Phase 2 (placeholder) --------
        else:
            st.info(
                "Phase 2 (Archaeological / Ancient Tamil) "
                "will be implemented in the next step."
            )








