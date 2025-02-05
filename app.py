# Libraries:
import streamlit as st
from openai import OpenAI  # We continue using the same library, but now with a custom base_url
import shelve
from PIL import Image
import pathlib
import time
import re
import markdown
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import datetime
import pytz
from urllib.parse import quote

# Page config:
st.set_page_config(
    page_title="Shaped AI, Osebni Inštruktor Matematike",
    page_icon=r"shaped-logo.png"
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
# ----- Sidebar Customization and Styling -----
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

        /* GeoGebra container styling */
        .geogebra-container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            overflow: visible;
        }
        .geogebra-container iframe {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid #e4e4e4;
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

if st.sidebar.button(" ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**NOV KLEPET** ‎ ‎ ‎ ‎ ‎  ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎", key="pulse"):
    # Reset chat history
    st.session_state.messages = []
    st.session_state.animated_messages = set()
    st.session_state.last_animated_index = -1
    st.rerun()

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
    <div class="subtle-text">You are currently running Shaped AI 2.1 made by slacker, Shaped AI © 2024</div>
    """,
    unsafe_allow_html=True
)
# ----- Define Avatars and DeepSeek Client -----
USER_AVATAR = "👤"
BOT_AVATAR = "top-logo.png"

# IMPORTANT: Change the client initialization to use DeepSeek v3.
client = OpenAI(
    api_key='sk-fcd0c54da9824560a6fd8a93bb546d50',         # Replace with your DeepSeek API key
    base_url="https://api.deepseek.com"        # Set the DeepSeek base URL
)
st.markdown(
    """
<style>
div[data-testid="stDialog"] div[role="dialog"]:has(.big-dialog) {
    width: 60vw;
    height: 600vh;
}
</style>
""",
    unsafe_allow_html=True,
)

# Set up the session state
if "openai_model" not in st.session_state:
    st.toast("You are currently running Shaped AI 2.1", icon="⚙️")
    # Change the model name to DeepSeek's model
    st.session_state["openai_model"] = "deepseek-chat"
    @st.dialog(" ")
    def vote():
        st.image("shaped-main.png")
        st.html("<span class='big-dialog'></span>")
    vote()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----- Greeting Functions -----
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
    
    .mode-display {{
        font-size: 20px;
        font-weight: bold;
        font-family: 'Raleway', sans-serif;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 40px;
        margin-left: -14px;
        color: #f5f5f5;
    }}
    </style>
    <div class="custom-greeting">{greeting}</div>
""", unsafe_allow_html=True)

# Display the selected mode under the greeting
mode_display = MODE.replace("**", "")
st.markdown(f'<div class="mode-display">{mode_display}</div>', unsafe_allow_html=True)

# ----- Display Functions -----
def type_response(content):
    message_placeholder = st.empty()
    full_response = ""
    for char in content:
        full_response += char
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.005)
    message_placeholder.markdown(full_response)

# ----- Add to session state setup -----
if "last_animated_index" not in st.session_state:
    st.session_state.last_animated_index = -1
# ----- Session State Setup -----
if "animated_messages" not in st.session_state:
    st.session_state.animated_messages = set()
# ----- Modified display functions -----
def display_response_with_geogebra(response_text, animate=True):
    parts = re.split(r'(##[^#]+##)', response_text)
    for part in parts:
        if part.startswith("##") and part.endswith("##"):
            function_command = part[2:-2].strip()
            encoded_function = quote(function_command)
            geogebra_url = f"https://www.geogebra.org/calculator?lang=en&command={encoded_function}"
            geogebra_html = f"""
            <div class="geogebra-container">
                <iframe src="{geogebra_url}" 
                        width="100%" 
                        height="450" 
                        allowfullscreen>
                </iframe>
            </div>
            """
            st.components.v1.html(geogebra_html, height=450)
        else:
            if animate:
                type_response(part)  # Animate only new responses
            else:
                st.markdown(part)  # Static display for older messages

def display_messages(messages):
    for index, message in enumerate(messages):
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                # Check if this message hasn't been animated yet
                if index not in st.session_state.animated_messages:
                    # Animate new response
                    display_response_with_geogebra(message["content"], animate=True)
                    st.session_state.animated_messages.add(index)
                else:
                    # Show static version for previously animated messages
                    display_response_with_geogebra(message["content"], animate=False)
            else:
                st.markdown(message["content"])

# ----- System Message Configuration -----
def get_system_message():
    graph_instructions = (
        "You are ShapedAI. You should speak slovenian unless asked otherwise. If you want to generate a graph, use a command enclosed in double hash symbols (##) To graph multiple functions separate them by using ; example: ##sin(x); x^2 ## "
        "For example ##x^2## or for a circle ##x^2 + y^2 = 1## Do not put latex inside the ## in the hash symbols; you can only place numbers, letters, =, +, -, sin(),* etc. As it will be displayed using this method: https://www.geogebra.org/calculator?lang=en&command={what you type in the ##} The ## command will be replaced with the graph so the user should not be aware of its existence. !DO NOT FORGET!: In case every number, variable, equation, latex, coordinates and any symbols related with math are wrapped in $$ For example: $$a$$ or $$1$$ or $$2x + 3 = 1y$$ IMPORTANT: You can't create a smiley face or other shapes; only circles and graphs. You can generate an empty GeoGebra window with: ## ## Again, the user should not know this command exists."
    )
    mode = st.session_state.mode
    if mode == "**⚡ Takojšnji odgovor**":
        return {
            "role": "system",
            "content": f"You are Shaped AI, a Slovenian math tutor. Provide direct solutions using LaTeX, still provide a step by step tutorial.  {graph_instructions}"
        }
    elif mode == "**📚 Filozofski način**":
        return {
            "role": "system",
            "content": f"Guide users step-by-step using Socratic questioning. Ask one question at a time. {graph_instructions}"
        }
    elif mode == "**😎 Gen Alpha način**":
        return {
            "role": "system",
            "content": f"U have to use skibidi, fr, cap, aura, low taper fade, brainrot, rizz and other slang in every response. You need to use this slang everywhere, be creative! Example: 'Nah fam, that equation's looking sus, let's fix that rizz' {graph_instructions} IMPORTANT!: You still need to reply in slovene just use this type of slang!"
        }

# ----- Main Logic -----
display_messages(st.session_state.messages)

# Process new user input
if prompt := st.chat_input("Kako lahko pomagam?"):
    # Add user message and trigger immediate display
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.generate_response = True
    st.rerun()

# Generate AI response after user message is displayed
if st.session_state.get("generate_response"):
    with st.spinner("Razmišljam..."):
        # Use the DeepSeek API to generate the chat completion
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[get_system_message()] + st.session_state.messages,
            stream=False  # Change stream as needed
        ).choices[0].message.content
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    del st.session_state.generate_response
    st.rerun()
