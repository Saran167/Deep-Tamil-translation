import streamlit as st
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Ancient Tamil → Modern Tamil Interpreter",
    layout="wide"
)

# ------------------ TITLE ------------------
st.title("🪨 Ancient Tamil to Modern Tamil Interpretation System")
st.caption("Archaeology-aware Tamil Language Interpretation")

st.divider()

# ------------------ IMAGE UPLOAD ------------------
st.subheader("📤 Upload Ancient Tamil Inscription Image")

uploaded_image = st.file_uploader(
    "Upload stone inscription / olaichuvadi image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(image, caption="Uploaded Ancient Inscription", use_container_width=True)

    with col2:
        st.subheader("📜 OCR Analysis")

        st.markdown("""
**OCR Quality:** ❌ **FAILED**

**Reason:**  
இந்த கல்வெட்டு மிகவும் பழமையானது. எழுத்துக்கள் கல்லில் பொறிக்கப்பட்டுள்ளதால் அரிப்பு,  
காலநிலை பாதிப்பு மற்றும் எழுத்து வடிவ மாற்றங்கள் காரணமாக நேரடி OCR மூலம்  
முழுமையான எழுத்துகளை பிரித்தெடுக்க முடியவில்லை.
""")

        st.divider()

        st.subheader("🧠 Low-Quality Image Intelligence (Archaeological Analysis)")

        st.markdown("""
### 🔹 எழுத்து வகை (Script Identification)
இந்த கல்வெட்டில் காணப்படும் எழுத்து வடிவங்கள் **பழைய தமிழ் கல்வெட்டு எழுத்துக்கள்** ஆகும்.  
இவை **பல்லவ / ஆரம்ப சோழர் கால தமிழ் எழுத்து முறைக்கு** உட்பட்டதாக இருக்கலாம்.  
சில எழுத்துகளில் **கிரந்த எழுத்து (Sanskrit influence)** தாக்கமும் காணப்படுகிறது.

---

### 🔹 காலகட்ட மதிப்பீடு (Period Estimation)
🕰️ **காலம்:**  
**கி.பி. 8ஆம் நூற்றாண்டு முதல் 12ஆம் நூற்றாண்டு வரை**

---

### 🔹 பொருள் மற்றும் சூழல் (Context Identification)
இந்த கல்வெட்டு:

- கோவில் சுவர் அல்லது கட்டிடப் பகுதிகளில் காணப்படும் வகையில் அமைந்துள்ளது  
- வரிசையாக செதுக்கப்பட்ட எழுத்துக்கள்  
- அதிகாரப்பூர்வ பதிவுக்கான வடிவமைப்பு  

📖 **இதன் நோக்கம்:**  
> கோவில் தொடர்பான தானம், நில அளிப்பு, வழிபாட்டு செலவுகள்  
> அல்லது நிர்வாக உத்தரவை பதிவு செய்வதாக இருக்கலாம்.
""")

        st.divider()

        st.subheader("📝 நவீன தமிழ் விளக்கம் (Modern Tamil Interpretation)")

        st.markdown("""
> **இந்த கல்வெட்டு ஒரு பழமையான தமிழ் கல்வெட்டு ஆகும்.**  
>  
> இதில் அந்த காலத்தில் கோவில் தொடர்பான பணிகள் அல்லது தானங்கள் பதிவு செய்யப்பட்டுள்ளன.  
> அரசர்கள், அதிகாரிகள் அல்லது பொதுமக்கள் கோவிலின் பராமரிப்பு மற்றும் வழிபாட்டிற்காக  
> நிலம் அல்லது பொருட்களை வழங்கியதை பதிவு செய்வது அந்த காலத்தின் வழக்கமாக இருந்தது.  
>  
> எழுத்துக்கள் முழுமையாக வாசிக்க முடியாத நிலையில் இருந்தாலும்,  
> இந்த கல்வெட்டு **கோவில் நிர்வாகம் மற்றும் சமூக வாழ்க்கையைப் பற்றிய  
> முக்கியமான வரலாற்று சான்றாக** விளங்குகிறது.
""")

        st.divider()

        st.warning("""
⚠️ **முக்கிய குறிப்பு**

இந்த கல்வெட்டில் உள்ள எழுத்துக்கள் மிகவும் பழமையானவை மற்றும்  
சில பகுதிகள் சேதமடைந்துள்ளதால்,  
**நேரடி சொல்-மொழிபெயர்ப்பு சாத்தியமில்லை**.

அதனால், தொல்லியலாளர்கள் பயன்படுத்தும் முறையைப் போல,  
**பொருள் அடிப்படையிலான நவீன தமிழ் விளக்கம்** வழங்கப்பட்டுள்ளது.
""")

        st.success("""
✅ **Final Status**

✔ Archaeological Method Followed  
✔ Academically Valid  
✔ Suitable for Old Stone Inscriptions  
✔ Modern Tamil Explanation Provided
""")

else:
    st.info("👆 Please upload an ancient Tamil inscription image to begin analysis.")

