# Libraries:
import streamlit as st
import requests
from deep_translator import GoogleTranslator
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
st.sidebar.image("shaped-ai.png", use_column_width=True)
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
    st.session_state.messages_display = []
    st.session_state.messages_model = []
    st.session_state.animated_messages = set()
    st.session_state.last_animated_index = -1
    st.rerun()

st.sidebar.markdown(
    """
    <style>
    .subtle-text {
        color: rgba(255, 255, 255, 0.3);
        font-size: 12px;
        text-align: center;
        margin-top: 6px;
    }
    </style>
    <div class="subtle-text">You are currently running Shaped AI 1.3 made by slacker, Shaped AI © 2024</div>
    """,
    unsafe_allow_html=True
)

# ----- Define Avatars and DeepSeek Client -----
USER_AVATAR = "👤"
BOT_AVATAR = "top-logo.png"
DEEPSEEK_API_KEY = "sk-5cb67cdc41514069b9e36333ce5d8ef6"  # Replace with your actual API key

# Set up the session state
if "openai_model" not in st.session_state:
    st.toast("You are currently running Shaped AI 2.1", icon="⚙️")
    st.session_state["openai_model"] = "deepseek-chat"

if "messages_display" not in st.session_state:
    st.session_state.messages_display = []
    
if "messages_model" not in st.session_state:
    st.session_state.messages_model = []

if "animated_messages" not in st.session_state:
    st.session_state.animated_messages = set()

if "last_animated_index" not in st.session_state:
    st.session_state.last_animated_index = -1

# ----- Translation Functions -----
def translate_response(response_en):
    parts = re.split(r'(\$\$.*?\$\$|##.*?##)', response_en, flags=re.DOTALL)
    translated_parts = []
    for part in parts:
        if part.startswith('$$') and part.endswith('$$'):
            translated_parts.append(part)
        elif part.startswith('##') and part.endswith('##'):
            translated_parts.append(part)
        else:
            if part.strip():
                try:
                    translated = GoogleTranslator(source='en', target='sl').translate(part)
                    translated_parts.append(translated)
                except:
                    translated_parts.append(part)
            else:
                translated_parts.append(part)
    return ''.join(translated_parts)

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
                type_response(part)
            else:
                st.markdown(part)

def display_messages(messages):
    for index, message in enumerate(messages):
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                if index not in st.session_state.animated_messages:
                    display_response_with_geogebra(message["content"], animate=True)
                    st.session_state.animated_messages.add(index)
                else:
                    display_response_with_geogebra(message["content"], animate=False)
            else:
                st.markdown(message["content"])

# ----- System Message Configuration -----
def get_system_message():
    graph_instructions = (
        "You are ShapedAI. If you want to generate a graph, use a command enclosed in double hash symbols (##) To graph multiple funtions seperate them by using ; example: ##sin(x); x^2 ## "
        "For example ##x^2## or for a circle ##x^2 + y^2 = 1## Do not put latex inside the ## in the hash symbols you can only place numbers, letters, =, +, -, sin(),* etc. As it will be displayed using this method: https://www.geogebra.org/calculator?lang=en&command={what you type in the ##} The ## command will be replaced with the graph so the user should not be aware of its existence. !DO NOT FORGET!: Incase every number, variable, equation, latex, cordinates and any symbols related with math in $$ For example: $$a$$ or $$1$$ or $$2x + 3 = 1y$$ IMPORATANT: you cant create smiley face or other shapes only circle and graphs. You can generate an empty geogebra window with: ## ## Again the user should not know this command exists."
    )
    mode = st.session_state.mode
    if mode == "**⚡ Takojšnji odgovor**":
        return {
            "role": "system",
            "content": f"You are a math tutor. Provide direct solutions using LaTeX. {graph_instructions}"
        }
    elif mode == "**📚 Filozofski način**":
        return {
            "role": "system",
            "content": f"Guide users step-by-step using Socratic questioning. {graph_instructions}"
        }
    elif mode == "**😎 Gen Alpha način**":
        return {
            "role": "system",
            "content": f"Use Gen Alpha slang like 'skibidi', 'fr', 'cap' etc. but keep response in English. {graph_instructions}"
        }

# ----- DeepSeek API Call -----
def get_deepseek_response(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Accept": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [get_system_message()] + messages,
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error contacting DeepSeek API: {str(e)}")
        return "Prišlo je do napake. Prosimo, poskusite znova."

# ----- Main Logic -----
display_messages(st.session_state.messages_display)

# Process new user input
if prompt := st.chat_input("Kako lahko pomagam?"):
    # Add to display messages
    st.session_state.messages_display.append({"role": "user", "content": prompt})
    # Translate and add to model messages
    try:
        translated_prompt = GoogleTranslator(source='sl', target='en').translate(prompt)
        st.session_state.messages_model.append({"role": "user", "content": translated_prompt})
    except:
        st.session_state.messages_model.append({"role": "user", "content": prompt})
    st.session_state.generate_response = True
    st.rerun()

# Generate AI response
if st.session_state.get("generate_response"):
    with st.spinner("Razmišljam..."):
        response_en = get_deepseek_response(st.session_state.messages_model)
        response_sl = translate_response(response_en)
        
        # Add to both message stores
        st.session_state.messages_model.append({"role": "assistant", "content": response_en})
        st.session_state.messages_display.append({"role": "assistant", "content": response_sl})
        
    del st.session_state.generate_response
    st.rerun()
