import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import time

st.set_page_config(page_title="Kannada to Hindi Translator", layout="wide")
st.title("🌐 Learn Hindi using Kannada Script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

@st.cache_data(show_spinner=False)
def translate_sentence(kannada_text):
    # Step 1: Kannada → Hindi (Devanagari)
    hindi = GoogleTranslator(source='kn', target='hi').translate(kannada_text)

    # Step 2: Hindi → Kannada phonetic
    try:
        hindi_in_kannada = transliterate(hindi, sanscript.DEVANAGARI, sanscript.KANNADA)
    except Exception:
        hindi_in_kannada = "Transliteration error"

    # Step 3: Hindi → English phonetic
    try:
        hindi_in_english = transliterate(hindi, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception:
        hindi_in_english = "Phonetic not available"

    return hindi, hindi_in_kannada, hindi_in_english


text = st.text_area("Enter Kannada text (e.g., ಬಾ ಇಲ್ಲಿಗೆ ಈಗ):", height=120)

if st.button("Translate"):
    if text.strip():
        with st.spinner("Translating... Please wait"):
            start = time.time()
            hindi, kannada_script, english_phonetic = translate_sentence(text)
            end = time.time()

        st.success(f"✅ Translation completed in {end - start:.2f} sec")
        st.subheader("Hindi Translation (Devanagari):")
        st.write(hindi)
        st.subheader("Hindi in Kannada Letters (Phonetic):")
        st.write(kannada_script)
        st.subheader("Hindi in English Phonetics:")
        st.write(english_phonetic)
    else:
        st.warning("Please enter some Kannada text.")
