# Libraries:
import streamlit as st
from openai import OpenAI
import shelve
from PIL import Image
import openai

#Hide all unneeded parts of streamlit:
st.set_page_config(
    page_title="Shaped-AI, free personal tutor.",
    page_icon=r"shaped-logo.png"
)
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

st.sidebar.image(r"shaped-ai.png", use_column_width=True)
st.markdown("""
    <style>
        .stApp {
            background-color: #2b2b2b;
        }
    </style>
    """, unsafe_allow_html=True) 
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
    <div class="mode-text">AI TUTOR MODE</div>
""", unsafe_allow_html=True)

