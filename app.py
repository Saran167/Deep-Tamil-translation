from core.translator import translate_to_tamil
from core.simplifier import simple_tamil, people_friendly_tamil

st.set_page_config(page_title="Tamil Simplification System")

st.title("Tamil Language Simplification System")

st.write(
    "Enter text in **any language**. "
    "The system translates it to Tamil and converts it into "
    "simple, people-friendly Tamil."
)

input_text = st.text_area("Enter your text", height=180)

if st.button("Convert"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            tamil_text = translate_to_tamil(input_text)

        if tamil_text == "":
            st.error("Translation failed. Please try again.")
        else:
            st.subheader("Machine Translated Tamil")
            st.write(tamil_text)

            simple = simple_tamil(tamil_text)
            friendly = people_friendly_tamil(simple)

            st.subheader("Simple Tamil")
            st.write(simple)

            st.subheader("People-Friendly Tamil")
            st.write(friendly)









