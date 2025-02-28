import streamlit as st
@st.dialog("Maintanance break!")
def dialog():
  st.write("We will be back shortly!")
dialog()

import streamlit as st
import requests

# Check if user is verified
if 'verified' not in st.session_state:
    st.session_state.verified = False

# Your reCAPTCHA keys (get from Google)
RECAPTCHA_SITE_KEY = "6LcwWuUqAAAAAH0TGgld65wlLxsUGFcXCLghjYrD"    # Replace with your actual key
RECAPTCHA_SECRET_KEY = "6LcwWuUqAAAAACy8G2i6rIg1FqzqxcHtTH_asD96"  # Replace with your actual key

if not st.session_state.verified:
    st.title("Verify You're Human")

    # Create reCAPTCHA widget using HTML
    captcha_html = f"""
    <html>
    <head>
        <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    </head>
    <body>
        <form id="captcha-form">
            <div class="g-recaptcha" 
                data-sitekey="{RECAPTCHA_SITE_KEY}"
                data-callback="onSubmit">
            </div>
            <button type="submit">Verify</button>
        </form>
        <script>
            function onSubmit(token) {{
                window.parent.postMessage({{
                    type: "captchaToken",
                    token: token
                }}, "*");
            }}
        </script>
    </body>
    </html>
    """

    # Display the captcha
    with st.form("captcha_form"):
        components.html(captcha_html, height=300)
        submitted = st.form_submit_button("Submit Verification")
    
    # Handle verification
    if submitted:
        # Get token from frontend
        token = st.experimental_get_query_params().get("token", [None])[0]
        
        if token:
            # Verify with Google
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    'secret': RECAPTCHA_SECRET_KEY,
                    'response': token
                }
            ).json()
            
            if response.get('success'):
                st.session_state.verified = True
                st.experimental_rerun()
            else:
                st.error("Verification failed. Please try again.")
        else:
            st.error("Please complete the captcha")
            
    st.stop()

# Your main app content here
st.write("Welcome to the app! You're verified!")
