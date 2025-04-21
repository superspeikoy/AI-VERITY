import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Ensure the 'UsageData' directory exists
os.makedirs('UsageData', exist_ok=True)

if 'signedin' in st.session_state and st.session_state.signedin:

    st.markdown('# Usage History 🕵️')
    st.divider()

    # Function to load and display usage data
    def load_usage_data(file_path, columns):
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=columns)

    # Define paths for different usage data files
    news_usage_data_path = r'UsageData\news_usage_data.csv'
    weather_usage_data_path = r'UsageData\weather_usage_data.csv'
    translator_usage_data_path = r'UsageData/translator_usage_data.csv'
    imagegen_usage_data_path = r'UsageData/imagegen_usage_data.csv'
    pptgen_usage_data_path = r'UsageData/pptgen_usage_data.csv'
    bot_usage_data_path = r'UsageData/chatbot_usage_data.csv'
    dashboard_usage_data_path = r'UsageData/dashboard_usage_data.csv'

    # Load the usage data for all services
    n_usage_data = load_usage_data(news_usage_data_path, ['Country', 'Category', 'Timestamp'])
    w_usage_data = load_usage_data(weather_usage_data_path, ['City', 'Temperature', 'Timestamp'])
    t_usage_data = load_usage_data(translator_usage_data_path, ['Source Lang','Destination Lang', 'Text','Translation','Timestamp'])
    i_usage_data = load_usage_data(imagegen_usage_data_path, ['Prompt','image','Timestamp'])
    p_usage_data = load_usage_data(pptgen_usage_data_path, ['Prompt','slides','Timestamp'])
    b_usage_data = load_usage_data(bot_usage_data_path, ['Prompt','Response','Timestamp'])
    d_usage_data = load_usage_data(dashboard_usage_data_path, ['UploadedFile','Timestamp'])

    # Display Usage Data and Graph for each service
    services = [
        ("News Wave 📰", n_usage_data, ['Country', 'Category']),
        ("Weather Vista ☁️", w_usage_data, ['City', 'Temperature']),
        ("Linguo Verse 🌐", t_usage_data, ['Source Lang','Destination Lang', 'Text', 'Translation']),
        ("Vision Vertex 🖼️", i_usage_data, ['Prompt','image']),
        ("Slide Craft 🎓", p_usage_data, ['Prompt','slides']),
        ("Bot Buddy 🤖", b_usage_data, ['Prompt','Response']),
        ("Sales Dashboard 📊", d_usage_data, ['UploadedFile'])
    ]

    for service_name, usage_data, group_by_columns in services:
        st.markdown(f'## Usage Data for {service_name}:')
        st.write(usage_data)

        if not usage_data.empty:
            try:
                # Grouping and plotting
                visit_counts = usage_data.groupby(group_by_columns)['Timestamp'].count().reset_index()
                visit_counts.set_index(group_by_columns, inplace=True)
                visit_counts.reset_index(inplace=True)
                st.bar_chart(visit_counts)
            except KeyError as e:
                st.error(f"An error occurred: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning(f"Usage data for {service_name} is empty. No chart to display.")

        st.divider()

else:
    st.warning("Please sign in to view the usage history.")
