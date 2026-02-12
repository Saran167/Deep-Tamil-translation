import streamlit as st
from indictrans_translator import translate_text
from confidence import calculate_confidence
from core.ancient_converter import convert_ancient_text

st.set_page_config(page_title="Ancient Tamil → Modern Tamil", layout="centered")

st.title("Ancient Tamil → Modern Tamil Translator")

text = st.text_area("Enter Ancient Tamil Text")

if st.button("Translate"):

    if text.strip() == "":
        st.warning("Enter some text")
    else:
        rule_output = convert_ancient_text(text)
        model_output = translate_text(text)

        confidence = calculate_confidence(text, model_output)

        st.subheader("Modern Tamil")
        st.write(model_output)

        st.subheader("Dictionary Match (if available)")
        st.write(rule_output)

        st.subheader("Confidence Score")
        st.write(confidence)






