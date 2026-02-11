import streamlit as st
import tempfile
import json
from gtts import gTTS

# Core modules
from core.translator import translate_to_tamil
from core.simplifier import simple_tamil, people_friendly_tamil
from core.ancient_converter import convert_ancient_text
from core.inscription_normalizer import normalize_stone_text
from core.confidence import calculate_confidence

# -----------------------------------

st.set_page_config(page_title="Tamil Language Processing System")

st.title("🪔 Tamil Language Processing System")
st.write("Multilingual Translation + Tamil Simplification + Archaeological Tamil Processing")

# -----------------------------------
# Mode Selection
# -----------------------------------

mode = st.selectbox(
    "Select Processing Mode",
    [
        "Any Language → Simple Tamil",
        "Ancient / Archaeological Tamil → Modern Tamil"
    ]
)

# -----------------------------------
# Input
# -----------------------------------

input_text = st.text_area("Enter your text", height=180)

# -----------------------------------
# PROCESS BUTTON
# -----------------------------------

if st.button("Process"):

    if input_text.strip() == "":
        st.warning("Please enter some text.")

    else:

        # =========================================
        # MODE 1 — ANY LANGUAGE → SIMPLE TAMIL
        # =========================================

        if mode == "Any Language → Simple Tamil":

            with st.spinner("Translating to Tamil..."):
                tamil_text = translate_to_tamil(input_text)

            if tamil_text == "":
                st.error("Translation failed. Check internet or API.")
            else:
                st.subheader("Machine Translated Tamil")
                st.write(tamil_text)

                simple = simple_tamil(tamil_text)
                friendly = people_friendly_tamil(simple)

                st.subheader("People-Friendly Tamil")
                st.write(friendly)

                # Voice output
                st.subheader("Tamil Voice Output")
                tts = gTTS(text=friendly, lang="ta")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)

        # =========================================
        # MODE 2 — ARCHAEOLOGICAL PIPELINE
        # =========================================

        else:

            st.subheader("Archaeological Processing Pipeline")

            # STEP 1 — Stone inscription normalization
            normalized = normalize_stone_text(input_text)

            st.subheader("Step 1: Normalized Text")
            st.write(normalized)

            # STEP 2 — Ancient word conversion
            modern_text, detected_terms = convert_ancient_text(normalized)

            st.subheader("Step 2: Modern Tamil Output")
            st.write(modern_text)

            # STEP 3 — Detected archaeological terms
            if detected_terms:
                st.subheader("Step 3: Detected Archaeological Terms")

                for term in detected_terms:
                    st.write(
                        f"• {term['ancient']} → {term['modern']} "
                        f"(Meaning: {term['meaning']}, Origin: {term['origin']})"
                    )
            else:
                st.info("No archaeological terms detected.")

            # STEP 4 — Confidence Score
            total_words = len(input_text.split())
            matched_words = len(detected_terms)

            confidence = calculate_confidence(total_words, matched_words)

            st.subheader("Step 4: Conversion Confidence")
            st.write(f"{confidence}%")

            # STEP 5 — Voice output
            st.subheader("Tamil Voice Output")
            tts = gTTS(text=modern_text, lang="ta")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)

            # STEP 6 — Dataset Viewer
            st.subheader("Research Dataset")

            if st.checkbox("Show Ancient Tamil Dataset"):

                try:
                    with open("data/ancient_dataset.json", encoding="utf-8") as f:
                        dataset = json.load(f)

                    for item in dataset:
                        st.write("Ancient:", item["ancient"])
                        st.write("Modern:", item["modern"])
                        st.write("Source:", item["source"])
                        st.write("---")

                except:
                    st.error("Dataset file not found. Check data folder.")



