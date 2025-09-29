import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process

st.title("Learn Hindi using Kannada script- ಕನ್ನಡ  ಅಕ್ಷರ  ಬಳಸಿ   ಹಿಂದಿ  ಕಲಿಯಿರಿ")

text = st.text_area("Enter Kannada text")

if st.button("Translate"):
    if text.strip():
        try:
            # Step 1: Kannada → Hindi translation
            hindi = GoogleTranslator(source="kn", target="hi").translate(text)

            # Step 2: Hindi → English phonetics (IAST)
            hindi_english = transliterate(hindi, sanscript.DEVANAGARI, sanscript.ITRANS)

            # Step 3: Hindi → Kannada script (sound copy)
            hindi_in_kannada = process('Devanagari', 'Kannada', hindi)

            # Output
            st.subheader("Results")
            st.write("**Kannada Input:**", text)
            st.write("**Hindi Translation:**", hindi)
            st.write("**Hindi in Kannada letters:**", hindi_in_kannada)
            st.write("**Hindi in English phonetics:**", hindi_english)

        except Exception as e:
            st.error(f"Error: {e}")
