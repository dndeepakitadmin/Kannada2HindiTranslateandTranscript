import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as indic_transliterate

st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="centered")
st.title("Learn Hindi using Kannada script - ಕನ್ನಡ ಅಕ್ಷರಗಳಲ್ಲಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# -------------------------------
# 🧠 Caching Section
# -------------------------------
@st.cache_data(show_spinner=False)
def translate_text(text):
    """Translate Kannada → Hindi → Phonetic → Kannada letters"""
    # Step 1: Translate Kannada → Hindi
    hindi_translation = GoogleTranslator(source='kn', target='hi').translate(text)

    # Step 2: Hindi → English phonetic
    hindi_phonetic = indic_transliterate(hindi_translation, sanscript.DEVANAGARI, sanscript.ITRANS)

    # Step 3: Hindi → Kannada-like letters (approx phonetic using ITRANS)
    hindi_in_kannada = indic_transliterate(hindi_translation, sanscript.DEVANAGARI, sanscript.KANNADA)

    return hindi_in_kannada, hindi_phonetic, hindi_translation


# -------------------------------
# 🧾 Streamlit UI
# -------------------------------
text = st.text_area("Enter Kannada text (ಉದಾ: ನೀವು ಹೇಗಿದ್ದೀರಿ ?):", height=100)

if st.button("Translate"):
    if text.strip():
        try:
            hindi_in_kannada, hindi_phonetic, hindi_translation = translate_text(text)

            st.markdown("### 🔹 Translation Results")
            st.markdown(f"**Kannada Input:** {text}")
            st.markdown(f"**Hindi in Kannada Letters:** {hindi_in_kannada}")
            st.markdown(f"**English Phonetic:** `{hindi_phonetic}`")
            st.markdown(f"**Hindi Translation (Devanagari):** {hindi_translation}")

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
    else:
        st.warning("⚠️ Please enter some Kannada text.")
