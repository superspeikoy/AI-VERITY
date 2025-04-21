import streamlit as st
import asyncio
from googletrans import Translator
from languages import *  # Assuming this is a list of supported languages
import os
import pandas as pd
from datetime import datetime

# Check if user is signed in
if 'signedin' in st.session_state and st.session_state.signedin:
    usage_data_path = r'UsageData/translator_usage_data.csv'
    
    # Load usage data from CSV if it exists, else create an empty DataFrame
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Source Lang', 'Destination Lang', 'Text', 'Translation', 'Timestamp'])

    # Set up Streamlit UI configuration
    st.set_page_config(page_title="Linguo Verse", page_icon="🌐", layout="wide")
    st.markdown("# Linguo Verse 🌐")
    st.sidebar.header("Linguo Verse 🌐")

    # Select source and target languages and input text for translation
    source_language = st.selectbox("Select source language:", languages)
    source_text = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Select target language:", languages)
    
    # Button to trigger translation
    translate = st.button('Translate')

    # Perform translation when the button is pressed
    if translate:
        # Validate that the source text is not empty
        if not source_text.strip():
            st.error("Please enter text to translate.")
        else:
            with st.spinner('Translating Text...'):
                try:
                    # Initialize Translator object
                    translator = Translator()
                    
                    # Use asyncio to await the translation (asynchronously)
                    async def get_translation():
                        # Perform the translation asynchronously
                        translation = await translator.translate(source_text, src=source_language, dest=target_language)
                        return translation.text
                    
                    # Execute the coroutine and get the result
                    translated_text = asyncio.run(get_translation())
                    
                    # Display the translated text
                    st.markdown("## Translated Text :")
                    st.write(translated_text)

                    # Save the translation details to the usage data DataFrame
                    new_entry = {
                        'Source Lang': source_language,
                        'Destination Lang': target_language,
                        'Text': source_text,
                        'Translation': translated_text,
                        'Timestamp': datetime.now()
                    }

                    # Use pd.concat to append the new entry
                    usage_data = pd.concat([usage_data, pd.DataFrame([new_entry])], ignore_index=True)

                    # Save the updated data to the CSV file
                    usage_data.to_csv(usage_data_path, index=False)

                except Exception as e:
                    # Handle errors like network issues or unsupported languages
                    st.error(f"An error occurred: {e}")

else:
    # Notify the user to sign in
    st.warning("Please sign in to translate the text.")
