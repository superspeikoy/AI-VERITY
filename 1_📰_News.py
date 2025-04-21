import streamlit as st
import pycountry
import requests
import pandas as pd
import os
from datetime import datetime
from api import NewsapiKey

# Ensure session state is set for signed-in users
if 'signedin' not in st.session_state:
    st.session_state.signedin = False

# If the user is signed in, proceed
if st.session_state.signedin:
    st.set_page_config(page_title="News Wave", page_icon="📰", layout="wide")
    st.markdown("# News Wave 📰")
    st.sidebar.header("News Wave 📰")

    # Define path for saving usage data
    usage_data_path = os.path.join(os.getcwd(), 'UsageData', 'news_usage_data.csv')
    os.makedirs(os.path.dirname(usage_data_path), exist_ok=True)

    # Load or initialize usage data
    if os.path.exists(usage_data_path):
        usage_data = pd.read_csv(usage_data_path)
    else:
        usage_data = pd.DataFrame(columns=['Country', 'Category', 'Timestamp'])

    # UI for country selection and news category
    col1, col2 = st.columns([3, 1])
    with col1:
        country_list = [country.name for country in pycountry.countries]
        selected_country = st.selectbox("Select Country:", country_list, index=country_list.index("India"))
    with col2:
        news_category = st.radio("Choose a news category", ('Technology', 'General', 'Health', 'Sports', 'Business'))
        btn = st.button("Get News")

    # Fetch and display news when button is pressed
    if btn:
        country = pycountry.countries.get(name=selected_country)
        if country:
            country_code = country.alpha_2
            with st.spinner('Fetching news...'):
                url = f"https://newsapi.org/v2/top-headlines?country={country_code}&category={news_category}&apiKey={NewsapiKey}"
                response = requests.get(url)
                if response.status_code == 200:
                    news_data = response.json()
                    if 'articles' in news_data and news_data['articles']:
                        for article in news_data['articles']:
                            # Display article details
                            st.header(article.get('title', 'No Title'))
                            st.write(f"Published at: {article.get('publishedAt', 'Unknown')}")
                            st.write(f"Author: {article.get('author', 'Unknown')}")
                            st.write(f"Source: {article['source'].get('name', 'Unknown')}")
                            
                            # Display image if available
                            if article.get('urlToImage'):
                                st.image(article['urlToImage'])
                            
                            # Safely handle the content and remove '...'
                            content = article.get('content', "No content available.")
                            if content:
                                st.write(content.replace('...', ''))
                            else:
                                st.write("No content available.")
                            
                            # Link to read more
                            st.write(f"Read more: [here]({article['url']})")
                        
                        # Save the user's search data for future reference
                        usage_data = pd.concat([usage_data, pd.DataFrame([{
                            'Country': selected_country,
                            'Category': news_category,
                            'Timestamp': datetime.now()
                        }])], ignore_index=True)
                        usage_data.to_csv(usage_data_path, index=False)

                    else:
                        st.warning("No articles found for this category.")
                else:
                    st.error(f"Failed to fetch news: {response.status_code} - {response.reason}")
        else:
            st.warning(f"Country '{selected_country}' not recognized.")
else:
    st.warning("Please sign in to view the news.")
