# Libraries:
import streamlit as st
from openai import OpenAI
import shelve
from PIL import Image
import pathlib
from openai import OpenAI
import time
import re
import markdown
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import datetime
import pytz

# Page config:
st.set_page_config(
    page_title="Shaped AI, Osebni Matematični Inštruktor",
    page_icon=r"top-logo.png"
)

# Load css from assets
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")
css_path = pathlib.Path("assets.css")
load_css(css_path)

# Hide all unneeded parts of streamlit:
hide_streamlit_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
hide_streamlit_style = """
<style>
div[data-testid="stToolbar"] {
visibility: hidden;
height: 0%;
position: fixed;
}
div[data-testid="stDecoration"] {
visibility: hidden;
height: 0%;
position: fixed;
}
div[data-testid="stStatusWidget"] {
visibility: hidden;
height: 0%;
position: fixed;
}
#MainMenu {
visibility: hidden;
height: 0%;
}
header {
visibility: hidden;
height: 0%;
}
footer {
visibility: hidden;
height: 0%;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.markdown('''
<style>
.stApp [data-testid="stToolbar"]{
    display:none;
}
</style>
''', unsafe_allow_html=True)
enable_scroll = """
<style>
.main {
    overflow: auto;
}
</style>
"""
st.markdown(enable_scroll, unsafe_allow_html=True)

# MAIN---------------------------------------------------------------------------------------------------------------------------:
    
# Sidebar styling
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1a2431;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0;
        }
        .sidebar .image-container img {
            margin-top: 0;
            margin-bottom: 0 !important;
        }
        
        /* Tight divider styling */
        .sidebar-divider {
            border: 1px solid #FF5733;
            margin: 0 0 5px 0 !important;
        }
        
        /* Header styling */
        .sidebar-header {
            font-size: 1.5rem !important;
            text-align: center !important;
            color: white !important;
            margin: 10px 0 15px 0 !important;
            font-weight: 700 !important;
            display: block !important;
            width: 100% !important;
        }
        
        /* Radio button styling */
        div[role="radiogroup"] {
            margin-top: 15px !important;
        }
        div[role="radiogroup"] label {
            border: 2px solid #FF5733;
            border-radius: 8px;
            padding: 8px 16px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }
        div[role="radiogroup"] label:hover {
            border-color: #FF5733;
            background-color: #0f1116;
        }
        div[role="radiogroup"] input:checked + label {
            border-color: #28a745;
            background-color: #d4f8e1;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# Add image to sidebar with tight divider
st.sidebar.image("shaped-ai.png", use_container_width=True)
st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
# Centered About button

# Add mode selection radio buttons to sidebar with working header
MODE = st.sidebar.radio(
    "‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ **Način Inštrukcije**",
    ["**📚 Filozofski način**: Tvoj AI inštruktor te bo vodil skozi probleme z izzivalnimi vprašanji. Ta pristop spodbuja kritično mišljenje in globlje razumevanje konceptov.",
     "**⚡ Takojšnji odgovor**: Tvoj AI inštruktor bo dal neposredne odgovore na tvoje vprašanje. Ta pristop se osredotoča na zagotavljanje natančnih rešitev z minimalnimi koraki razlage.",
     "**😎 Gen Alpha način**: Fr fr, matematika razložena s strani tvojega giga možganov chad inštruktorja, ki ti dviguje matematično auro, no cap."],
    index=0,
    key="mode",
    help="Izberi način učenja, ki ti najbolj ustreza", # This was missing for header rendering
)
st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

USER_AVATAR = "👤"
BOT_AVATAR = r"top-logo.png"
client = OpenAI(api_key='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')

# Set up the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to determine Slovenian time and greet
def get_slovene_greeting():
    slovenia_tz = pytz.timezone('Europe/Ljubljana')
    local_time = datetime.datetime.now(slovenia_tz)
    
    if 5 <= local_time.hour < 12:
        return "Dobro jutro🌅"
    elif 12 <= local_time.hour < 18:
        return "Dober dan☀️"
    else:
        return "Dober večer🌙"

# Display the greeting with updated style
greeting = get_slovene_greeting()

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');
    .custom-greeting {{
        font-size: 40px;
        font-weight: bold;
        font-family: 'Raleway', sans-serif;
        text-align: center;
        margin-top: -20px; 
        margin-bottom: 10px;
    }}
    
    .fade-in-out {{
        animation: fadeInOut 1.5s ease-in-out infinite;
    }}
    
    @keyframes fadeInOut {{
        0% {{
            opacity: 0;
        }}
        50% {{
            opacity: 0.9;
        }}
        100% {{
            opacity: 0;
        }}
    }}
    </style>
    <div class="custom-greeting">{greeting}</div>
""", unsafe_allow_html=True)

# Typing animation function
def type_response(content):
    message_placeholder = st.empty()
    full_response = ""
    for char in content:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.005)
    message_placeholder.markdown(full_response)

# Function to find and render LaTeX using st.markdown
def render_latex(text):
    parts = re.split(r'(\$\$[^\$]+\$\$)', text)
    rendered_parts = []
    for i, part in enumerate(parts):
        if part.startswith("$$") and part.endswith("$$"):
            rendered_parts.append(f"<div style='text-align:left;'>{part[2:-2]}</div>")
        else:
            rendered_parts.append(part)
    return "".join(rendered_parts)

def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Show existing messages
display_messages(st.session_state.messages)

# Response mode functions
def get_system_message():
    mode = st.session_state.mode
    if mode == "**⚡ Takojšnji odgovor**: Tvoj AI inštruktor bo dal neposredne odgovore na tvoje vprašanje. Ta pristop se osredotoča na zagotavljanje natančnih rešitev z minimalnimi koraki razlage.":
        return {
            "role": "system",
            "content": (
                "You are Shaped AI, a Slovenian math expert. Provide direct solutions using LaTeX for all math. "
                "Be concise. Example: 'Rešitev je $$x = 5$$. Respond in Slovenian unless asked otherwise." "Every math symbol, equation, letter, number has to be incased in $$. For example $$a$$ or $$x + 2$$ Thats how the program knows it has to show it as latex!"
            )
        }
    elif mode == "**📚 Filozofski način**: Tvoj AI inštruktor te bo vodil skozi probleme z izzivalnimi vprašanji. Ta pristop spodbuja kritično mišljenje in globlje razumevanje konceptov.":
        return {
            "role": "system",
            "content": (
                "You are a patient math tutor. Guide users step-by-step using Socratic questioning. "
                "Ask one question at a time. Use LaTeX for all math. Respond in Slovenian unless asked otherwise.""Every math symbol, equation, letter, number has to be incased in $$. For example $$a$$ or $$x + 2$$ Thats how the program knows it has to show it as latex!"
            )
        }
    elif mode == "**😎 Gen Alpha način**: Fr fr, matematika razložena s strani tvojega giga možganov chad inštruktorja, ki ti dviguje matematično auro, no cap.":
        return {
            "role": "system",
            "content": (
                "Explain math like a Slovenian friend using slang (skibidi toilet, aura, cap, fr, slovenian slang etc.). Keep it casual but accurate. "
                "Example: 'To je easy, samo uporabiš $$E=mc^2$$.' Use LaTeX for all math. Avoid formal terms." "Every math symbol, equation, letter, number has to be incased in $$. For example $$a$$ or $$x + 2$$ Thats how the program knows it has to show it as latex!"
            )
        }

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Show "thinking" animation
    thinking_message = st.empty()
    thinking_message.markdown('<div class="fade-in-out">‎Razmišljam...</div>', unsafe_allow_html=True)

    # Get response from the AI model
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[get_system_message()] + st.session_state.messages
    ).choices[0].message.content

    # Update chat and remove thinking message
    thinking_message.empty()
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        type_response(response)
