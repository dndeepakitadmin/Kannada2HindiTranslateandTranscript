import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process

st.set_page_config(page_title="Kannada to Hindi Learning", layout="centered")

st.title("📝 Learn Hindi using Kannada script")
st.subheader("ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# Input
text = st.text_area("Enter Kannada text here...", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # Kannada → Hindi
            hindi = GoogleTranslator(source="kn", target="hi").translate(text)

            # Hindi → English phonetics (IAST)
            hindi_english = transliterate(hindi, sanscript.DEVANAGARI, sanscript.ITRANS)

            # Hindi → Kannada script
            hindi_in_kannada = process('Devanagari', 'Kannada', hindi)

            # ---------------- OUTPUT ---------------- #
            st.markdown("### 🔹 Translation Results")

            # Kannada Input
            st.markdown(f"**Kannada Input:**  \n:blue[{text}]")

            # Hindi Translation
            st.markdown(f"**Hindi Translation:**  \n:green[{hindi}]")

            # Hindi in Kannada script
            st.markdown(f"**Hindi in Kannada letters:**  \n:orange[{hindi_in_kannada}]")

            # Hindi in English phonetics
            st.markdown(f"**Hindi in English phonetics:**  \n`{hindi_english}`")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some Kannada text to translate!")
