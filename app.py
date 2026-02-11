import streamlit as st
import tempfile
import json
import sys
import os
from gtts import gTTS

# -----------------------------------
# FIX FOR STREAMLIT CLOUD IMPORT PATH
# -----------------------------------

sys.path.append(os.path.join(os.path.dirname(__file__), "core"))

# Import core modules
from translator import translate_to_tamil
from simplifier import simple_tamil, people_friendly_tamil
from ancient_converter import convert_ancient_text
from inscription_normalizer import normalize_stone_text
from confidence import calculate_confidence

# -----------------------------------

st.set_page_config(page_title="Tamil Language Processing System")

st.title("🪔 Tamil Language Processing System")
st.write("Multilingual Translation + Tamil Simplification + Archaeological Tamil Processing")

# -----------------------------------
# MODE SELECTION
# -----------------------------------

mode = st.selectbox(
    "Select Processing Mode",
    [
        "Any Language → Simple Tamil",
        "Ancient / Archaeological Tamil → Modern Tamil"
    ]
)

# -----------------------------------
# INPUT BOX
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
                st.error("Translation failed. Check internet.")
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

            # STEP 1 — Normalize stone text
            normalized = normalize_stone_text(input_text)

            st.subheader("Step 1: Normalized Text")
            st.write(normalized)

            # STEP 2 — Convert ancient words
            modern_text, detected_terms = convert_ancient_text(normalized)

            st.subheader("Step 2: Modern Tamil Output")
            st.write(modern_text)

            # STEP 3 — Detected terms
            if detected_terms:
                st.subheader("Step 3: Detected Archaeological Terms")

                for term in detected_terms:
                    st.write(
                        f"• {term['ancient']} → {term['modern']} "
                        f"(Meaning: {term['meaning']}, Origin: {term['origin']})"
                    )
            else:
                st.info("No archaeological terms detected.")

            # STEP 4 — Confidence score
            total_words = len(input_text.split())
            matched_words = len(detected_terms)

            confidence = calculate_confidence(total_words, matched_words)

            st.subheader("Step 4: Conversion Confidence")
            st.write(f"{confidence}%")

            # STEP 5 — Voice output
            st.subheader("Tamil Voice Output")

            if modern_text.strip() != "":
                tts = gTTS(text=modern_text, lang="ta")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)

            # STEP 6 — Dataset viewer
            st.subheader("Research Dataset")

            if st.checkbox("Show Ancient Tamil Dataset"):

                try:
                    dataset_path = os.path.join("data", "ancient_dataset.json")

                    with open(dataset_path, encoding="utf-8") as f:
                        dataset = json.load(f)

                    for item in dataset:
                        st.write("Ancient:", item["ancient"])
                        st.write("Modern:", item["modern"])
                        st.write("Source:", item["source"])
                        st.write("---")

                except Exception as e:
                    st.error("Dataset file not found. Check data folder.")




