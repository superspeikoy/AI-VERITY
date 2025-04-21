import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime
from api import Unsplash_key  # Replace Openai_key with Unsplash_key

if 'signedin' in st.session_state and st.session_state.signedin:

    st.set_page_config(page_title="Vision Vortex", page_icon="🖼️", layout="wide")
    st.markdown("# Vision Vortex 🖼️")
    st.sidebar.header("Vision Vortex 🖼️")

    usage_data_path = r'UsageData/imagegen_usage_data.csv'
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Prompt', 'Image URL', 'Timestamp'])

    def fetch_images_from_unsplash(query):
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1"
        headers = {"Authorization": f"Client-ID {Unsplash_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']  # Return the image URL
        return None

    input_prompt = st.text_area("Enter your text prompt", placeholder="Enter the image description you want to search")
    generate_image = st.button('Search')
    if generate_image:
        with st.spinner('Searching for Image...'):
            image_url = fetch_images_from_unsplash(input_prompt)
            if image_url:
                st.image(image_url, caption=f"{input_prompt} - Image from Unsplash")
                usage_data = usage_data._append({'Prompt': input_prompt, 'Image URL': image_url, 'Timestamp': datetime.now()}, ignore_index=True)
                usage_data.to_csv(usage_data_path, index=False)
                st.session_state['image_url'] = image_url
            else:
                st.error("No images found. Try a different prompt.")

    if st.button("Regenerate"):
        with st.spinner('Searching for Image...'):
            image_url = fetch_images_from_unsplash(input_prompt)
            if image_url:
                st.image(image_url, caption=f"{input_prompt} - Image from Unsplash")
                st.session_state['image_url'] = image_url
            else:
                st.error("No images found. Try a different prompt.")

    if st.button("Download"):
        if 'image_url' in st.session_state:
            download_link = f'<a href="{st.session_state["image_url"]}" download="unsplash_image.png">Download Image</a>'
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.warning("Please search for an image first before downloading.")
else:
    st.warning("Please sign in to search images.")
