# Libraries:
import streamlit as st
from openai import OpenAI
import shelve
from PIL import Image
from openai import OpenAI
import pathlib
#page config:
st.set_page_config(
    page_title="Shaped AI, Personal AI Tutor",
    page_icon=r"shaped-logo.png"
)

#Load css from assets
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")
css_path = pathlib.Path("assets.css")
load_css(css_path)
    
#Hide all unneeded parts of streamlit:
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

#main:
# Sidebar styling
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #191919;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0;
        }
        .sidebar .image-container img {
            margin-top: 0;
        }
    </style>
    """, unsafe_allow_html=True)

# Add image to sidebar
st.sidebar.image("shaped-ai.png", use_container_width=True)

# Main app background color
st.markdown("""
    <style>
        .stApp {
            background-color: #2b2b2b;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar divider and text
st.sidebar.markdown("""
    <style>
        .divider {
            border-bottom: 1px solid #4a4a4a;
            margin: 15px 0;
        }
        .mode-text {
            color: #666666;
            text-align: center;
            font-family: Arial;
            font-size: 14px;
            margin: 10px 0;
        }
    </style>
    
    <div class="divider"></div>
    <div class="mode-text">AI TUTOR</div>
""", unsafe_allow_html=True)

# Initialize session state for selected button
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None

# Function to handle button clicks
def handle_button_click(button_id):
    st.session_state.selected_button = button_id

# Button container
st.sidebar.markdown('<div class="button-container">', unsafe_allow_html=True)

# Math button
math_selected = "selected" if st.session_state.selected_button == "math" else ""
st.sidebar.button("➕", key="math", on_click=handle_button_click, args=("math",))
st.sidebar.markdown(f'<div class="button-label">Math</div>', unsafe_allow_html=True)

# Chemistry button
chemistry_selected = "selected" if st.session_state.selected_button == "chemistry" else ""
st.sidebar.button("⚗️", key="chemistry", on_click=handle_button_click, args=("chemistry",))
st.sidebar.markdown(f'<div class="button-label">Chemistry</div>', unsafe_allow_html=True)

# Physics button
physics_selected = "selected" if st.session_state.selected_button == "physics" else ""
st.sidebar.button("⚛️", key="physics", on_click=handle_button_click, args=("physics",))
st.sidebar.markdown(f'<div class="button-label">Physics</div>', unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Display selected button
if st.session_state.selected_button:
    st.sidebar.text(f"Selected: {st.session_state.selected_button.capitalize()}")
else:
    st.sidebar.text("No selection yet")
