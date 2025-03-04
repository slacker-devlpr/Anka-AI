# Libraries:
import streamlit as st
from openai import OpenAI  
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
import json
from google import genai
from google.genai import types
from captcha.image import ImageCaptcha
import random
import string
from streamlit_cropper import st_cropper

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



# Define CAPTCHA constants
length_captcha = 4
width = 200
height = 150




       
# Define the function for CAPTCHA control
def captcha_control():
    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        st.session_state.language = "Slovene"
        # Language selection dialog
        st.image("Screenshot 2025-03-01 123153.png")
        options = ["Slovenščina", "English"]
        selection = st.selectbox(
        "Please select your language / Prosimo, izberite svoj jezik.", options)
        if selection == "Slovenščina":
            st.session_state.language = "Slovene"
        if selection == "English":
            st.session_state.language = "English"
        st.write("  ")
        st.write("  ")
        if st.session_state.language == "Slovene":
            st.write("Zaradi velikega števila botov, ki preplavljajo našo spletno stran, morate izpolniti to CAPTCHA, da dokažete, da ste človek.")
        else:
            st.write("Due to a large number of bots flooding our website, you need to complete this CAPTCHA to prove you are human.")
        st.write(" ")
        # Define the session state for control if the CAPTCHA is correct
        st.session_state['controllo'] = False
        col1, col2 = st.columns(2)
        
        # Define the session state for the CAPTCHA text because it doesn't change during refreshes 
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))
        print("the CAPTCHA is: ", st.session_state['Captcha'])
        
        # Setup the CAPTCHA widget
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        if st.session_state.language == "Slovene":
            capta2_text = col2.text_area(' ', height=68, max_chars=4, placeholder="tukaj napiši katere simbole vidiš na sliki", help="Na sliki so lahko črke in/ali številke.")
        else:
            capta2_text = col2.text_area(' ', height=68, max_chars=4, placeholder="enter the symbols you see in the image", help="The image may contain letters and/or numbers.")

        
        if col2.button("Potrdi" if st.session_state.language == "Slovene" else "Confirm", use_container_width=True):
            print(capta2_text, st.session_state['Captcha'])
            capta2_text = capta2_text.replace(" ", "")
            # If the CAPTCHA is correct, the controllo session state is set to True
            if st.session_state['Captcha'].lower() == capta2_text.lower().strip():
                del st.session_state['Captcha']
                col1.empty()
                col2.empty()
                st.session_state['controllo'] = True
                st.rerun()  # Automatically redirect to the main app
            else:
                # If the CAPTCHA is wrong, the controllo session state is set to False and the CAPTCHA is regenerated
                if st.session_state.language == "Slovene":
                    st.error("Poskusite še enkrat.")
                else:
                    st.error("Please try again.")
                del st.session_state['Captcha']
                del st.session_state['controllo']
                st.rerun()
        else:
            # Wait for the button click
            st.stop()

# Main logic
if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
    captcha_control()
    
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
st.sidebar.markdown(
    """
    <style>
    /* Center the radio group container */
    div[data-baseweb="radio"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* Center each radio option label */
    div[data-baseweb="radio"] label {
        text-align: center;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center the label and radio button group
if st.session_state.language == "Slovene":
    MODE = st.sidebar.radio(
        "‎**Način Inštrukcije**",
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
        help="Izberi način inštrukcije, ki ti najbolj ustreza",
    )
else:
    MODE = st.sidebar.radio(
        "‎**Instruction Mode**",
        options=[
            "**📚 Philosophical Mode**",
            "**⚡ Instant Answer**",
            "**😎 Gen Alpha Mode**"
        ],
        captions=[
            "Your AI tutor will guide you through problems with challenging questions. This approach encourages critical thinking and deeper understanding of concepts.",
            "Your AI tutor will provide direct answers to your questions. This approach focuses on providing accurate solutions with minimal explanation steps.",
            "Fr fr, math explained by your big brain chad tutor, boosting your math aura, no cap."
        ],
        index=0,
        key="mode",
        help="Select the instruction mode that suits you best",
    )

st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

# Ensure session state variables are initialized
if "show_camera_dialog" not in st.session_state:
    st.session_state.show_camera_dialog = False
if "processing_image" not in st.session_state:
    st.session_state.processing_image = False
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None  # Store the captured image
if "layout" not in st.session_state:
    st.session_state.layout = True

# Sidebar button to open the camera dialog
col1, col2, col3 = st.sidebar.columns([1, 6, 1])
with col2:
    if st.button(
        "NALOŽI SLIKO" if st.session_state.get("language", "English") == "Slovene" else "UPLOAD IMAGE",
        key="camera_btn",
        use_container_width=True,
    ):
        st.session_state.show_camera_dialog = True
        st.rerun()  # Ensure UI updates

st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

# Handle Camera Dialog
if st.session_state.show_camera_dialog:
    @st.dialog(
        "Slikaj matematični problem:" if st.session_state.get("language", "English") == "Slovene" else "Capture Math Problem:"
    )
    def camera_dialog():
        # Step 1: Show camera input only if no image is captured
        if st.session_state.captured_image is None:
            picture = st.camera_input(
                " ")

            if picture is not None:
                st.session_state.captured_image = picture
                st.session_state.layout = False  # Hide camera input
                st.rerun()  # Rerun to refresh UI

        # Step 2: Show cropping tool if an image is captured
        if st.session_state.captured_image is not None:
            st.write("Označi samo eno nalogo:" if st.session_state.get("language", "English") == "Slovene" else "Select only one problem:")
            image = Image.open(st.session_state.captured_image)  # Convert to PIL Image
            cropped_image = st_cropper(image, realtime_update=True, box_color="#FF0000", aspect_ratio=None)
            if st.button("Prekliči" if st.session_state.get("language", "English") == "Slovene" else "Cancel", use_container_width=True):
                st.session_state.show_camera_dialog = False
                st.session_state.captured_image = None
                st.rerun()
                
           
            if st.button("Nadaljuj" if st.session_state.get("language", "English") == "Slovene" else "Countinue", use_container_width=True):
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                cropped_image.save(img_byte_arr, format="PNG")
                st.session_state.image_to_process = img_byte_arr.getvalue()

                # Reset state and close dialog
                st.session_state.show_camera_dialog = False
                st.session_state.captured_image = None  # Clear stored image
                st.session_state.processing_image = True
                st.rerun()

    camera_dialog()

# Process image after dialog closes
if st.session_state.get("processing_image", False):
    with st.spinner("Procesiram sliko..." if st.session_state.language == "Slovene" else "Processing image..."):
        try:
            # Initialize Gemini client
            gemini_client = genai.Client(api_key=str(st.secrets["gemini_api"]) ) # Replace with your API key

            # Get response from Gemini
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash-latest",
                contents=[
                    "Extract the problem from this image, try to extract everybit of text. You can use č and š as you will be detecting slovene text. Do not solve it though. Only reply with the extracted text/problem(if visual try to describe the visual part in slovene). Never add any other added response message to it, only the description/extracted text!. Provide extremly detailed descriptions of visual parts of the problem(like graphs ect.). If the image doesnt incude a problem say: #error.user#. If theres a table DRAW IT NOT DESCRIBE IT(you have to be carefull with tables every empty/filled square matters, so if one is empty you MUST add that square even if it seems unecessary!). If there is more than one problem pick the one that covers most of the screen. Vedno Ilustriraj tabele ne opisi! Enclose every number, variable, equation, LaTeX, coordinates, and any math-related symbols in $$. For example: $$a$$ or $$1$$ or $$2x + 3 = 1y$$. Do not forget to extract the instructions of the problem!" if st.session_state.language == "Slovene" else "Extract the problem from this image, try to extract everybit of text. Do not solve it though. Only reply with the extracted text/problem(if visual try to describe the visual part in english). Never add any other added response message to it, only the description/extracted text!. Provide extremly detailed descriptions of visual parts of the problem(like graphs ect.).  If the image doesnt incude a problem say: #error.user#. If theres a table DRAW IT NOT DESCRIBE IT(you have to be carefull with tables every empty/filled square matters). If there is more than one problem pick the one that covers most of the screen. Always ilustrate tables not describe!  Enclose every number, variable, equation, LaTeX, coordinates, and any math-related symbols in $$. For example: $$a$$ or $$1$$ or $$2x + 3 = 1y$$. Do not forget to extract the instructions of the problem!",
                    types.Part.from_bytes(data=st.session_state.image_to_process, mime_type="image/jpeg")
                ]
            )

            extracted_problem = response.text

            # Check if Gemini returned an error message
            if "#error.user#" in extracted_problem:
                st.error("test")
                st.rerun()
                
            else:
                # Add extracted problem to chat only if there is no error indicator
                st.session_state.messages.append({"role": "user", "content": extracted_problem})
                st.session_state.generate_response = True

        except Exception as e:
            st.error(f"Napaka pri obdelavi slike: {str(e)}" if st.session_state.language == "Slovene" else f"Error processing image: {str(e)}")
            st.session_state.messages.append({"role": "error", "content": f"Napaka pri obdelavi slike: {str(e)}" if st.session_state.language == "Slovene" else f"Error processing image: {str(e)}"})
        finally:
            # Clean up processing state
            st.session_state.processing_image = False
            if "image_to_process" in st.session_state:
                del st.session_state.image_to_process
            st.rerun()


scol1, scol2, scol3 = st.sidebar.columns([1,6,1])                  
with scol2:
    if st.button("NOV KLEPET" if st.session_state.language == "Slovene" else "NEW CHAT", key="pulse", use_container_width=True):
        # Reset chat history and other session state items
        st.session_state.messages = []
        st.session_state.animated_messages = set()
        st.session_state.last_animated_index = -1
        if "generate_response" in st.session_state:
            del st.session_state.generate_response
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
    <div class="subtle-text">Version 3.0</div>
    """,
    unsafe_allow_html=True
)
        
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
    <div class="subtle-text">Copyright © 2024 Shaped AI. All rights reserved.</div>
    """,
    unsafe_allow_html=True
)
# ----- Define Avatars and DeepSeek Client -----
ERROR = "⚠️"
USER_AVATAR = "👤"
BOT_AVATAR = "top-logo.png"

# IMPORTANT: Change the client initialization to use DeepSeek v3.
client = OpenAI(
    api_key=str(st.secrets["deepseek_api"]),        
    base_url="https://api.deepseek.com"        # Set the DeepSeek base URL
)
st.markdown(
    """
<style>
div[data-testid="stDialog"] div[role="dialog"]:has(.big-dialog) {
    width: 60vw;
    height: 125vh;
}
</style>
""",
    unsafe_allow_html=True,
)

# Set up the session state
if "openai_model" not in st.session_state:
    # Change the model name to DeepSeek's model
    st.session_state["openai_model"] = "deepseek-chat"
    @st.dialog("Dobrodošli👋" if st.session_state.language == "Slovene" else "Welcome👋")
    def vote():
        st.write("Shaped AI Inštruktor je eden prvih brezplačnih Matematičnih AI inštruktorjev, ki deluje kot neprofitna pobuda! 🎓🚀" if st.session_state.language == "Slovene" else "Shaped AI Tutor is one of the first free Math AI tutors operating as a non-profit initiative! 🎓🚀") 
        st.write(" ")
        st.write("Verjamemo, da bi morale biti inštrukcije matematike dostopne vsem – popolnoma brezplačno! 🧮💡" if st.session_state.language == "Slovene" else "We believe that math tutoring should be accessible to everyone – completely free! 🧮💡")
        st.write(" ")
        st.write("A čeprav so naše storitve brezplačne, njihovo delovanje ni – strežniki, materiali in čas zahtevajo sredstva. Če želite podpreti našo misijo, bomo izjemno hvaležni za BTC donacije čez BTC network na 1KB31MXN19KNMwFFsvwGyjkMdSku3NGgu9🙏💙" if st.session_state.language == "Slovene" else "Although our services are free, their operation is not – servers, materials, and time require resources. If you wish to support our mission, we would be extremely grateful for BTC donations via the BTC network to 1KB31MXN19KNMwFFsvwGyjkMdSku3NGgu9🙏💙")
        st.write(" ")
        st.write("📍 Živite v Ljubljani? Pokličite 031 577 600 in si zagotovite ena na ena inštrukcije v živo! 📞✨" if st.session_state.language == "Slovene" else "📍 Living in Ljubljana? Call 031 577 600 and secure one-on-one live tutoring! 📞✨")
        st.write("")
        st.image("MADE USING.jpg")
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

def get_english_greeting():
    slovenia_tz = pytz.timezone('Europe/Ljubljana')
    local_time = datetime.datetime.now(slovenia_tz)
    
    if 5 <= local_time.hour < 12:
        return "Good morning🌅"
    elif 12 <= local_time.hour < 18:
        return "Good afternoon☀️"
    else:
        return "Good evening🌙"

# Display the greeting with updated style
if st.session_state.language == "Slovene":
    greeting = get_slovene_greeting()
else:
    greeting = get_english_greeting()


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
        time.sleep(0.002)
    message_placeholder.markdown(full_response)

# ----- Add to session state setup -----
if "last_animated_index" not in st.session_state:
    st.session_state.last_animated_index = -1
# ----- Session State Setup -----
if "animated_messages" not in st.session_state:
    st.session_state.animated_messages = set()
# ----- Modified display functions -----
# ----- Modified display functions -----
def display_response_with_geogebra(response_text):
    """Simplified display without animation (handled by streaming)"""
    parts = re.split(r'(@@[^@]+@@)', response_text)
    for part in parts:
        if part.startswith("@@") and part.endswith("@@"):
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
            st.markdown(part)

def display_messages(messages):
    for index, message in enumerate(messages):
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        avatar = ERROR if message["role"] == "error" else avatar
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                display_response_with_geogebra(message["content"])
            else:
                st.markdown(message["content"])

# ... (keep session state and greeting code unchanged)

# ----- Main Logic -----
display_messages(st.session_state.messages)

# Process new user input
if prompt := st.chat_input("Kako lahko pomagam?" if st.session_state.language == "Slovene" else "How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.generate_response = True
    st.rerun()

# Streaming response handling
if st.session_state.get("generate_response"):
    try:
        # Add empty assistant message first
        st.session_state.messages.append({"role": "assistant", "content": ""})
        
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            
            # Start streaming
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[get_system_message()] + st.session_state.messages[:-1],
                stream=True
            )
            
            # Process chunks in real-time
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    st.session_state.messages[-1]["content"] = full_response
                    message_placeholder.markdown(full_response + "▌")
            
            # Final update without cursor
            message_placeholder.markdown(full_response)
            
            # Trigger rerun to process graphs
            st.rerun()
            
    except Exception as e:
        error_msg = "Napaka pri povezavi z API! " if st.session_state.language == "Slovene" else "API Connection Error! "
        st.session_state.messages.append({"role": "error", "content": error_msg + str(e)})
    finally:
        if "generate_response" in st.session_state:
            del st.session_state.generate_response
