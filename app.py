import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as indic_transliterate

# Primary transliteration engine (Aksharamukha)
try:
    from aksharamukha import transliterate as akshara_transliterate
    AKSHARAMUKHA_AVAILABLE = True
except Exception:
    AKSHARAMUKHA_AVAILABLE = False

# -----------------------------------------------------------
# ✅ Streamlit Page Setup
# -----------------------------------------------------------
st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="centered")
st.title("Learn Hindi using Kannada Script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")
st.markdown("Type Kannada sentences below and see Hindi in Kannada letters, Hindi script, and English phonetics.")

# -----------------------------------------------------------
# ⚡️ Caching-enabled Translation Functions
# -----------------------------------------------------------
@st.cache_data(show_spinner=False)
def translate_kannada_to_hindi(text: str) -> str:
    """Translate Kannada → Hindi using Deep Translator."""
    try:
        return GoogleTranslator(source="kn", target="hi").translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"


@st.cache_data(show_spinner=False)
def hindi_to_kannada_script(hindi_text: str) -> str:
    """Convert Hindi (Devanagari) → Kannada script (phonetic)."""
    try:
        if AKSHARAMUKHA_AVAILABLE:
            return akshara_transliterate.process("Devanagari", "Kannada", hindi_text)
        else:
            # Fallback using indic_transliteration approximate mapping
            return indic_transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.KANNADA)
    except Exception as e:
        return f"Kannada script conversion error: {str(e)}"


@st.cache_data(show_spinner=False)
def hindi_to_english_phonetic(hindi_text: str) -> str:
    """Convert Hindi (Devanagari) → English phonetic."""
    try:
        return indic_transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception as e:
        return f"Phonetic conversion error: {str(e)}"


# -----------------------------------------------------------
# 🧾 Streamlit UI
# -----------------------------------------------------------
text = st.text_area("✍️ Enter Kannada text (ಉದಾ: ನೀವು ಹೇಗಿದ್ದೀರಿ ?)", height=120)

if st.button("Translate & Convert"):
    if text.strip():
        with st.spinner("🔄 Translating... please wait"):
            # Step 1: Kannada → Hindi
            hindi_text = translate_kannada_to_hindi(text)

            # Step 2: Hindi → Kannada script (phonetic)
            hindi_in_kannada = hindi_to_kannada_script(hindi_text)

            # Step 3: Hindi → English phonetic
            english_phonetic = hindi_to_english_phonetic(hindi_text)

        # -------------------------------
        # ✅ Display Results
        # -------------------------------
        st.markdown("### 🔹 Translation Results")
        st.markdown(f"**Kannada Input:**  \n:blue[{text}]")
        st.markdown(f"**Hindi Translation (Devanagari):**  \n:green[{hindi_text}]")
        st.markdown(f"**Hindi in Kannada Letters (Phonetic):**  \n:orange[{hindi_in_kannada}]")
        st.markdown(f"**Hindi in English Phonetics:**  \n`{english_phonetic}`")

        st.success("✅ Translation completed successfully!")

    else:
        st.warning("⚠️ Please enter some Kannada text to translate.")

# -----------------------------------------------------------
# 📘 Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption("⚡ Powered by Streamlit | Google Translator | Aksharamukha | Indic Transliteration")
