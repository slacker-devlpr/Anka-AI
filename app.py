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
    page_title="Shaped AI, Osebni Inštruktor Matematike",
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

# Add mode selection radio buttons to sidebar with working header
MODE = st.sidebar.radio(
    "‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ **Način Inštrukcije**",
    options=[
        "**📚 Filozofski način**",
        "**⚡ Takojšnji odgovor**",
        "**😎 Gen Alpha način**"
    ],
    captions=[
        "Tvoj AI inštruktor te bo vodil skozi probleme z izzivalnimi vprašanji. Ta pristop spodbuja kritično mišljenje in globlje razumevanje konceptov.",
        "Tvoj AI inštruktor bo dal neposredne odgovore na tvoje vprašanje. Ta pristop se osredotoča na zagotavljanje natančnih rešitev z minimalnimi koraki razlage.",
        "Fr fr, matematika razložena s strani tvojega giga možganov chad inštruktorja, ki ti dviguje matematično auro, no cap."
    ],
    index=0,
    key="mode",
    help="Izberi način inštrukcije, ki ti najbolj ustreza"
)
st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

# Add "NOV KLEPET" button to reset the chat
if st.sidebar.button("‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ **NOV KLEPET** ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎  ", key="pulse", help="Klikni za začetek novega klepeta"):
    st.session_state.messages = []  # Clear chat history
    st.rerun()  # Rerun the app to reflect the changes

st.sidebar.markdown(
    """
    <style>
    .subtle-text {
        color: rgba(255, 255, 255, 0.3); /* White text with 30% opacity */
        font-size: 12px;
        text-align: center;
        margin-top: 6px; /* Adjust spacing as needed */
    }
    </style>
    <div class="subtle-text">You are currently running Shaped AI 1.3 powered by OpenAI and Streamlit, Shaped AI © 2024</div>
    """,
    unsafe_allow_html=True
)

# Define avatars and OpenAI client
USER_AVATAR = "👤"
BOT_AVATAR = "top-logo.png"
client = OpenAI(api_key='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')  # Replace with your OpenAI API key

# Set up the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

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
    
    .mode-display {{
        font-size: 20px;
        font-weight: bold;
        font-family: 'Raleway', sans-serif;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 40px;
        margin-left: -14px;
        color: #f5f5f5; /* Custom color for the mode text */
    }}
    </style>
    <div class="custom-greeting">{greeting}</div>
""", unsafe_allow_html=True)

# Display the selected mode under the greeting
mode_display = MODE.replace("**", "")  # Remove bold formatting for cleaner display
st.markdown(f'<div class="mode-display">{mode_display}</div>', unsafe_allow_html=True)

# Function to process GeoGebra embeds
def process_geogebra_embeds(text):
    """Detect ## notation and replace with GeoGebra iframes"""
    parts = re.split(r'##(.*?)##', text)
    processed = []
    graphs = []
    
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Odd elements are the graph expressions
            safe_expr = quote(part.strip())
            iframe = f"""
            <div style="margin: 15px 0; border-radius: 8px; overflow: hidden;">
                <iframe src="https://www.geogebra.org/graphing?input={safe_expr}" 
                        width="100%" 
                        height="400" 
                        style="border: 1px solid #2d4059;"
                        allowfullscreen>
                </iframe>
            </div>
            """
            graphs.append(iframe)
            processed.append(f"{{GRAPH_{len(graphs)-1}}}")
        else:
            processed.append(part)
    
    return "".join(processed), graphs

# Function to display messages with GeoGebra embeds
def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            processed_text, graphs = process_geogebra_embeds(message["content"])
            
            # Split text by graph placeholders
            text_parts = re.split(r'\{GRAPH_(\d+)\}', processed_text)
            
            for i, part in enumerate(text_parts):
                if i % 2 == 0:  # Regular text
                    st.markdown(part, unsafe_allow_html=True)
                else:  # Graph index
                    graph_index = int(part)
                    if graph_index < len(graphs):
                        st.markdown(graphs[graph_index], unsafe_allow_html=True)

# Typing animation function
def type_response(content):
    message_placeholder = st.empty()
    full_response = ""
    processed_content, graphs = process_geogebra_embeds(content)
    
    # Split content into text and graph placeholders
    parts = re.split(r'(\{GRAPH_\d+\})', processed_content)
    
    for part in parts:
        if re.match(r'\{GRAPH_\d+\}', part):
            # Handle graph insertion
            graph_index = int(re.search(r'\d+', part).group())
            if graph_index < len(graphs):
                message_placeholder.markdown(full_response + graphs[graph_index], unsafe_allow_html=True)
        else:
            # Handle text typing animation
            for char in part:
                full_response += char
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                time.sleep(0.005)
    
    message_placeholder.markdown(full_response, unsafe_allow_html=True)

# Initialize chat with welcome message
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Dobrodošel! Kako želiš, da te kličem?"
    }
    st.toast("We sincerely apologize for the slow response times. The API servers, powered by DeepSeek, are currently experiencing technical difficulties.", icon="⏳")
    st.session_state.messages.append(initial_message)

# Display existing messages
display_messages(st.session_state.messages)

# Response mode functions
def get_system_message():
    mode = st.session_state.mode
    graph_instruction = (
        "If visualization would help, generate graphs using ##function## notation. "
        "Example: 'Graf funkcije: ##x^2##'. Only one function per ## tags. "
        "Keep graphs relevant and simple."
    )
    
    if mode == "**⚡ Takojšnji odgovor**":
        return {
            "role": "system",
            "content": f"You are Shaped AI... {graph_instruction}"
        }
    elif mode == "**📚 Filozofski način**":
        return {
            "role": "system",
            "content": f"You are a patient math tutor... {graph_instruction}"
        }
    elif mode == "**😎 Gen Alpha način**":
        return {
            "role": "system",
            "content": f"You are a Slovenian slang tutor... {graph_instruction}"
        }

# Main chat interface
if prompt := st.chat_input("Kako lahko pomagam?"):
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
