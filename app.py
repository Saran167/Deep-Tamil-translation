import streamlit as st
from PIL import Image

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Simple Tamil Translator",
    page_icon="🧠",
    layout="wide"
)

# -------------------- APP HEADER --------------------
st.title("🧠 Dual-Phase Intelligent Tamil Translation System")
st.subheader("Phase 1: Any Language → Simple, People-Friendly Tamil")

st.markdown(
    """
    This phase converts **any language** into **simple modern Tamil**
    that common people can easily understand.
    """
)

st.divider()

# -------------------- INPUT TYPE SELECTION --------------------
st.markdown("### 📥 Choose Input Type")

input_type = st.radio(
    "Select how you want to give input:",
    ["Text", "Voice", "Image", "PDF"],
    horizontal=True
)

st.divider()

# -------------------- INPUT SECTION --------------------
input_text = None
uploaded_file = None

if input_type == "Text":
    input_text = st.text_area(
        "✍️ Enter text in any language:",
        height=200,
        placeholder="Type or paste text here..."
    )

elif input_type == "Voice":
    st.info("🎙️ Voice input will be converted to text")
    st.button("Start Recording (Coming Soon)")

elif input_type == "Image":
    uploaded_file = st.file_uploader(
        "📷 Upload Image",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

elif input_type == "PDF":
    uploaded_file = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )
    if uploaded_file:
        st.success(f"Uploaded file: {uploaded_file.name}")

st.divider()

# -------------------- PROCESS BUTTON --------------------
if st.button("🔄 Convert to Simple Tamil", type="primary"):

    with st.spinner("Processing... Please wait"):

        # Placeholder outputs
        detected_language = "Detected Automatically"
        extracted_text = "Extracted text will appear here"
        simple_tamil_output = "இது எளிய தமிழ் மொழிபெயர்ப்பு ஆகும்"

    st.success("Conversion Completed!")

    st.divider()

    # -------------------- OUTPUT SECTION --------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Original / Extracted Text")
        st.markdown(f"**Language:** {detected_language}")
        st.text_area(
            "Text",
            extracted_text,
            height=200
        )

    with col2:
        st.markdown("### ✅ Simple Modern Tamil Output")
        st.text_area(
            "Simplified Tamil",
            simple_tamil_output,
            height=200
        )

    st.divider()

    st.download_button(
        label="⬇️ Download Output",
        data=simple_tamil_output,
        file_name="simple_tamil_translation.txt",
        mime="text/plain"
    )

# -------------------- SIDEBAR --------------------
st.sidebar.title("ℹ️ About Phase 1")
st.sidebar.markdown(
    """
    **Phase 1 Features**
    - Any Language → Tamil
    - Simple spoken Tamil
    - Text, Voice, Image, PDF input
    - User-friendly output
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍🎓 Designed for common people & beginners")

