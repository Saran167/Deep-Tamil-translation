import streamlit as st
from core.translator import translate_to_tamil
from core.simplifier import simple_tamil, people_friendly_tamil
from core.ancient_converter import ancient_to_modern
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Tamil Language Processing System")

st.title("🪔 Tamil Language Processing System")

mode = st.selectbox(
    "Select Mode",
    [
        "Any Language → Simple Tamil",
        "Ancient / Archaeological Tamil → Modern Tamil"
    ]
)

input_text = st.text_area("Enter your text", height=180)

if st.button("Process"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        if mode == "Any Language → Simple Tamil":
            tamil_text = translate_to_tamil(input_text)
            if tamil_text == "":
                st.error("Translation failed.")
            else:
                simple = simple_tamil(tamil_text)
                friendly = people_friendly_tamil(simple)

                st.subheader("People-Friendly Tamil")
                st.write(friendly)

                tts = gTTS(text=friendly, lang="ta")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    st.audio(fp.name)

        else:
            modern = ancient_to_modern(input_text)

            st.subheader("Modern Tamil Output")
            st.write(modern)

            tts = gTTS(text=modern, lang="ta")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)



