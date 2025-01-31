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
            background-color: #1a2431;
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


USER_AVATAR = "👤"
BOT_AVATAR = r"shaped-logo.png"
client = OpenAI(api_key='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')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    parts = re.split(r'(\$\$[^\$]+\$\$)', text)  # Split at $$...$$ delimiters
    rendered_parts = []
    for i, part in enumerate(parts):
        if part.startswith("$$") and part.endswith("$$"):
            rendered_parts.append(f"<div style='text-align:left;'>{part[2:-2]}</div>") # This is the only change here from the previous code
        else:
            rendered_parts.append(part)
    return "".join(rendered_parts)

def display_messages(messages):
    for message in messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Add initial hello message if first visit
if not st.session_state.messages:
    initial_message = {
        "role": "assistant",
        "content": "Testing 2.1"
    }
    st.toast("Anka-AI is still in Beta. Expect mistakes!", icon="👨‍💻")
    st.toast("You are currently running Anka-AI 2.1.4.", icon="⚙️")
    st.session_state.messages.append(initial_message)

display_messages(st.session_state.messages)

# Function to generate and display plot
def generate_and_display_plot(function_string):
    try:
        # Generate Python code using OpenAI to plot the function
        plot_code_prompt = f"""
        Generate python code using matplotlib and numpy to plot the following mathematical function/instructions: {function_string}.
        Use 1000 data points, make it look clean, find a good ration for the y and x axis so that its clear to read.
        The plot should have a black background and for the axis white lines.
        If you need to generate geometric shapes use a plain background without axi.
        If asked to also generate geometric shapes. Make sure that if youre asked to make a climogram for the temp. to be a red smooth line and the rain/precipitation to be a blue bar for each month.
        Only generate the code block no additional text.
        """
        plot_code_response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": plot_code_prompt}]
        ).choices[0].message.content

        # Execute the generated code
        # First extract the code from the string
        match = re.search(r'```python\n(.*?)\n```', plot_code_response, re.DOTALL)
        if match:
            code_to_execute = match.group(1)
        else:
            code_to_execute = plot_code_response
            
        fig, ax = plt.subplots()
        
        # Set background color to black
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        
        # Set spines color to white
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        
        # Set axis tick colors to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Set axis label colors to white
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        exec(code_to_execute, globals(), locals())
        
        # Change plot line color to white if not set in code
        for line in ax.lines:
          if line.get_color() == 'C0':  # Check if default color
            line.set_color('white')
        
        # Set title color to white
        ax.title.set_color('white')
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png", facecolor=fig.get_facecolor())
        buf.seek(0)
        
        # Encode to base64 for display
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        
        # Display the plot in Streamlit
        st.markdown(f'<img src="data:image/png;base64,{image_base64}" alt="Plot">', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating plot: {e}")
        
    plt.close()
# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    if prompt.strip().lower() == "/plot":
        st.session_state.messages.append({"role":"assistant", "content": "Please enter the function to plot after the command `/plot` such as `/plot x^2`"})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            type_response("Please enter the function to plot after the command `/plot` such as `/plot x^2`")
    elif prompt.lower().startswith("/plot"):
        function_string = prompt[5:].strip()
        st.session_state.messages.append({"role":"assistant", "content": f"Generating a plot of function: {function_string}"})
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            type_response(f"Generating a plot of function: `{function_string}`")
        generate_and_display_plot(function_string)

    else:
        system_message = {
            "role": "system",
            "content": (
                "You are Anka-AI, a specialized artificial intelligence for assisting with mathematics. You were created by Gal Kokalj. "
                "Your primary goal is to help users understand and solve math problems."
                "For every math symbol, equation, or expression, no matter how simple it is use latex and surrond it by $$. For example $$a$$ is a part of the equation $$( 2x^3 - 4x^2 + 3x - 5 )$$. Every number, variable also has to be incased in $$, example: $$a$$"
                "You can plot any graph by using the command %%formula/instructions%% at the end and of your response(Make the graph of x squared. Example Great i'll create the graph for you. %%x squared%%. If you want to create a geometric shape/shapes that can contain color write the description like this: %%create a rectangle, circle, with a radius of... etc.%%"
                "Be concise and helpful. Use clear and simple terms to help the user learn math as easily as possible(use the most simple formulas possable for the problem). Do not mention you using $$ or %% commands as their are deleted out of your response and replaced by latex or a graph."
                "Note that in the history you won't see the commands for generating images/graphs, but that doesnt mean you dont have to use the command! Always put the command at the end of your sentence, and do not tell the user it exists (i will generate that for you: %%x squared%%"
                "You can also create a climogram, example: Create a climogram for the following information: jan: 13C° 100mm ect. "
            )
        }

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[system_message] + st.session_state.messages
        ).choices[0].message.content
        
        # Check for plot command
        plot_match = re.search(r'%%(.*?)%%', response)
        if plot_match:
            function_string = plot_match.group(1)
            
            # Remove %%formula%% from the response
            response = re.sub(r'%%.*?%%', '', response).strip()
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                type_response(response)
            
            generate_and_display_plot(function_string)
        else:
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant", avatar=BOT_AVATAR):
               type_response(response)
