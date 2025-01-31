import streamlit as st
import openai
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Shaped AI",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject custom CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #191919;
            color: white;
        }
        .stChatInput textarea {
            background-color: #2d2d2d !important;
            color: white !important;
        }
        .st-bq {
            background-color: #2d2d2d !important;
            border-radius: 15px !important;
        }
        .stChatMessage {
            padding: 10px;
            border-radius: 15px;
            margin: 10px 0;
        }
        .user-message {
            background-color: #2d2d2d !important;
        }
        .assistant-message {
            background-color: #404040 !important;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API key input
with st.sidebar:
    st.title("Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("[Get OpenAI API Key](https://platform.openai.com/account/api-keys)")

# Logo and header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    logo = Image.open("shaped-ai.png")
    st.image(logo, width=150)
    st.title("Shaped AI")

# Chat container
chat_container = st.container()

# Function to generate AI response
def generate_response(prompt):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message Shaped AI..."):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Generate AI response
    with st.spinner("Thinking..."):
        response = generate_response(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(response)
