import streamlit as st
from transformers import pipeline
import logging

# Logging setup
logging.basicConfig(level=logging.ERROR)

# Function to get the translation pipeline
@st.cache(allow_output_mutation=True)
def get_translator(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    try:
        return pipeline("translation", model=model_name)
    except Exception as e:
        logging.error(f"Pipeline creation failed: {e}")
        return None

def translate_text(text, src_lang, tgt_lang):
    translator = get_translator(src_lang, tgt_lang)
    if translator is None:
        return "Translation service is currently unavailable."
    try:
        translation = translator(text, max_length=512)
        return translation[0]['translation_text']
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return f"Error in translation: {str(e)}"

def main():
    st.title("Real-time Language Translation")

    # Static list of languages
    languages = {
        "English": "en", "Spanish": "es", "French": "fr", "German": "de",
        "Italian": "it", "Portuguese": "pt", "Dutch": "nl", "Russian": "ru"
    }

    src_lang = st.selectbox("Select source language", list(languages.keys()), index=0)
    tgt_lang = st.selectbox("Select target language", list(languages.keys()), index=1)

    text = st.text_area("Enter text to translate:", height=300, max_chars=1000)  # Character limit

    if st.button("Translate"):
        if text:
            with st.spinner('Translating...'):
                result = translate_text(text, languages[src_lang], languages[tgt_lang])
                if "Error in translation" in result:
                    st.error(result)
                else:
                    st.success(result)
        else:
            st.warning("Please enter some text to translate.")

    if st.button("Clear"):
        st.session_state.clear()

    # Usage instructions
    st.sidebar.write("Instructions: Select source and target languages, enter text, and click 'Translate'.")

    # Feedback mechanism
    if st.sidebar.button("Feedback"):
        st.sidebar.text_input("Leave your feedback here", key="feedback")

    # Session state management (example)
    if 'previous_translations' not in st.session_state:
        st.session_state['previous_translations'] = []

if __name__ == "__main__":
    main()