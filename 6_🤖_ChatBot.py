import streamlit as st
from google import genai

# Set page configuration for a polished look.
st.set_page_config(page_title="Chatbot 🤖", page_icon="🤖", layout="wide")
st.markdown("# Chatbot 🤖")

# Replace with your actual API key.
API_KEY = "AIzaSyD88Lo7FZ0k85GGjvSNePCVMrJFSHKlTP8"
client = genai.Client(api_key=API_KEY)

# Initialize conversation history in session state.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display conversation history using Streamlit's chat components.
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input using the chat input widget.
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Append the user's message to the conversation history.
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate a response from the Gemini model (gemini-2.0-flash).
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_input
    )
    bot_response = response.text.strip()
    
    # Append and display the assistant's reply.
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
