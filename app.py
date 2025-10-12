import streamlit as st
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from deep_translator import GoogleTranslator
import time

# --- Streamlit page setup ---
st.set_page_config(page_title="Kannada to Hindi Translator", layout="wide")
st.title("🌐 Learn Hindi using Kannada Script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# --- Cache setup for speed ---
@st.cache_data(show_spinner=False)
def translate_sentence(kannada_text):
    translator = Translator()
    try:
        # Step 1: Kannada → Hindi (Devanagari)
        hindi = translator.translate(kannada_text, src='kn', dest='hi').text
    except Exception:
        # fallback via deep_translator
        hindi = GoogleTranslator(source='kn', target='hi').translate(kannada_text)
    
    # Step 2: Hindi (Devanagari) → Kannada script phonetic
    try:
        hindi_in_kannada = transliterate(hindi, sanscript.DEVANAGARI, sanscript.KANNADA)
    except Exception:
        hindi_in_kannada = "Transliteration error"
    
    # Step 3: Hindi (Devanagari) → English phonetic
    try:
        hindi_in_english = transliterate(hindi, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception:
        hindi_in_english = "Phonetic not available"
    
    return hindi, hindi_in_kannada, hindi_in_english

# --- Input box ---
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
