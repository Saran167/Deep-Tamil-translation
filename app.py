import streamlit as st
from core.translator import translate_to_tamil
from core.simplifier import simple_tamil, people_friendly_tamil
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Any Language → Simple Tamil")

st.title("🌍 Any Language → Simple Tamil (with Voice)")

input_text = st.text_area("Enter your text", height=180)

if st.button("Convert"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            tamil_text = translate_to_tamil(input_text)

        if tamil_text == "":
            st.error("Translation failed.")
        else:
            st.subheader("Machine Translated Tamil")
            st.write(tamil_text)

            simple = simple_tamil(tamil_text)
            friendly = people_friendly_tamil(simple)

            st.subheader("People-Friendly Tamil")
            st.write(friendly)

            # 🔊 Voice Output
            st.subheader("Tamil Voice Output")

            tts = gTTS(text=friendly, lang="ta")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_file = fp.name

            st.audio(audio_file, format="audio/mp3")


