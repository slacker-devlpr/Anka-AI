import streamlit as st
import openai

# Set OpenAI API key (store securely in production)
openai.api_key = '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'

# Page config:
st.set_page_config(
    page_title="Shaped AI, Personal AI Tutor",
    page_icon=r"shaped-logo.png"
)

# Custom CSS for styling
st.markdown(f"""
    <style>
        .stApp {{
            background-color: #191919;
        }}
        .css-1d391kg {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 2rem;
        }}
        .stChatInput {{
            background-color: #2d2d2d;
            border-radius: 10px;
        }}
        .stTextInput input {{
            color: white !important;
        }}
        .message {{
            padding: 1rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            color: white;
            max-width: 80%;
        }}
        .user {{
            background-color: #2d2d2d;
            margin-left: auto;
        }}
        .assistant {{
            background-color: #404040;
            margin-right: auto;
        }}
        .logo {{
            text-align: center;
            margin-bottom: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

# Add logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("shaped-ai.png", width=200)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    css_class = "user" if role == "user" else "assistant"
    alignment = "right" if role == "user" else "left"
    
    st.markdown(f"""
        <div class="message {css_class}" style="text-align: {alignment};">
            {content}
        </div>
    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Message Shaped AI..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    st.markdown(f"""
        <div class="message user" style="text-align: right;">
            {prompt}
        </div>
    """, unsafe_allow_html=True)
    
    # Generate assistant response
    with st.spinner(''):
        response = openai.chat.compleations.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        msg = response.choices[0].message.content
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    # Display assistant response
    st.markdown(f"""
        <div class="message assistant" style="text-align: left;">
            {msg}
        </div>
    """, unsafe_allow_html=True)
