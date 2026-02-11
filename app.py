import streamlit as st
import tempfile
import json
from gtts import gTTS

# Import your custom IndicTrans module
from indictrans_translator import indictrans_translator

# Other imports
from simplifier import simple_tamil, people_friendly_tamil
from confidence import calculate_confidence

# -----------------------------------

st.set_page_config(page_title="Tamil Language Processing System")

st.title("🪔 Tamil Language Processing System")
st.write("Multilingual Translation + Tamil Simplification + Archaeological Tamil Processing")

mode = st.selectbox(
    "Select Processing Mode",
    [
        "Any Language → Simple Tamil",
        "Ancient / Archaeological Tamil → Modern Tamil"
    ]
)

input_text = st.text_area("Enter your text", height=180)

# -----------------------------------
# PROCESS BUTTON
# -----------------------------------

if st.button("Process"):

    if input_text.strip() == "":
        st.warning("Please enter some text.")
        st.stop()

    # =====================================
    # MODE 1 — ANY LANGUAGE → SIMPLE TAMIL
    # =====================================
    if mode == "Any Language → Simple Tamil":

        with st.spinner("Translating..."):
            tamil_text = indictrans_translator.translate(input_text, source_lang="auto", target_lang="ta")

        if tamil_text == "":
            st.error("Translation failed.")
        else:
            st.subheader("Machine Translated Tamil")
            st.write(tamil_text)

            simple = simple_tamil(tamil_text)
            friendly = people_friendly_tamil(simple)

            st.subheader("People-Friendly Tamil")
            st.write(friendly)

            st.subheader("Tamil Voice Output")
            tts = gTTS(text=friendly, lang="ta")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

    # =====================================
    # MODE 2 — ARCHAEOLOGY PIPELINE
    # =====================================
    else:

        st.subheader("Archaeological Processing Pipeline")

        normalized = normalize_stone_text(input_text)
        st.subheader("Step 1: Normalized Text")
        st.write(normalized)

        modern_text, detected_terms = convert_ancient_text(normalized)
        st.subheader("Step 2: Modern Tamil")
        st.write(modern_text)

        if detected_terms:
            st.subheader("Step 3: Detected Terms")
            for term in detected_terms:
                st.write(
                    f"{term['ancient']} → {term['modern']} "
                    f"(Meaning: {term['meaning']}, Origin: {term['origin']})"
                )
        else:
            st.info("No archaeological terms detected.")

        confidence = calculate_confidence(
            len(input_text.split()),
            len(detected_terms)
        )

        st.subheader("Step 4: Confidence")
        st.write(f"{confidence}%")

        st.subheader("Tamil Voice Output")
        if modern_text:
            tts = gTTS(text=modern_text, lang="ta")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

        if st.checkbox("Show Research Dataset"):
            try:
                with open("data/ancient_dataset.json", encoding="utf-8") as f:
                    dataset = json.load(f)

                for item in dataset:
                    st.write("Ancient:", item["ancient"])
                    st.write("Modern:", item["modern"])
                    st.write("Source:", item["source"])
                    st.write("---")

            except:
                st.error("Dataset not found.")






