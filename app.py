# Libraries:
import streamlit as st
from openai import OpenAI
import shelve
from PIL import Image
from openai import OpenAI
import pathlib

# Page config:
st.set_page_config(
    page_title="Shaped AI, Personal AI Tutor",
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

# Add image to sidebar with use_container_width instead of use_column_width
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
            font-size: 12px;
            letter-spacing: 2px;
            margin: 20px 0;
        }
    </style>
    
    <div class="divider"></div>
    <div class="mode-text">AI TUTOR</div>
""", unsafe_allow_html=True)

# Add three buttons next to each other in the sidebar
col1, col2, col3 = st.sidebar.columns(3)

with col1:
    if st.button("Button 1"):
        st.write("Button 1 clicked")

with col2:
    if st.button("Button 2"):
        st.write("Button 2 clicked")

with col3:
    if st.button("Button 3"):
        st.write("Button 3 clicked")
