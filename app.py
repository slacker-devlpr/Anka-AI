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
# Function to provide direct answer
def provide_answer():
    # Check if there is at least one message
    if not st.session_state.messages:
        return "Please ask a question first!"

    prompt = st.session_state.messages[-1]["content"]
    system_message = {
        "role": "system",
        "content": "You are Shaped AI, providing direct answers to mathematical problems in Slovenian."
    }
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[system_message, {"role": "user", "content": prompt}]
    ).choices[0].message.content
    return response

# Function to tutor step-by-step
def tutor_answer():
    # Check if there is at least one message
    if not st.session_state.messages:
        return "Please ask a question first!"

    prompt = st.session_state.messages[-1]["content"]
    system_message = {
        "role": "system",
        "content": "You are Shaped AI, tutoring users through mathematical problems in Slovenian with explanations step-by-step."
    }
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[system_message, {"role": "user", "content": prompt}]
    ).choices[0].message.content
    return response

# Function to explain in slang
def explain_slang():
    # Check if there is at least one message
    if not st.session_state.messages:
        return "Please ask a question first!"

    prompt = st.session_state.messages[-1]["content"]
    system_message = {
        "role": "system",
        "content": "You are Shaped AI, explaining mathematical problems in Slovenian using casual slang."
    }
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[system_message, {"role": "user", "content": prompt}]
    ).choices[0].message.content
    return response
