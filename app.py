import streamlit as st
@st.dialog("Maintanance break!")
def dialog():
  st.write("We will be back shortly!")
dialog()

from streamlit_recaptcha import recaptcha_component

# Initialize session state for captcha verification
if 'captcha_verified' not in st.session_state:
    st.session_state['captcha_verified'] = False

# Add your actual keys here (get them from Google reCAPTCHA)
RECAPTCHA_SITE_KEY = "6LcwWuUqAAAAAH0TGgld65wlLxsUGFcXCLghjYrD"          # Replace with your actual site key
RECAPTCHA_SECRET_KEY = "6LcwWuUqAAAAACy8G2i6rIg1FqzqxcHtTH_asD96"      # Replace with your actual secret key

if not st.session_state['captcha_verified']:
    st.title("Human Verification Required")
    
    # Display the reCAPTCHA widget
    recaptcha_response = recaptcha_component(site_key=RECAPTCHA_SITE_KEY)
    
    if recaptcha_response:
        # Verify the reCAPTCHA response (this would normally be done with Google's API)
        # For simplicity, we're just checking that a response exists here
        # In production, you should verify the response properly
        if recaptcha_response != "VERIFICATION_FAILED":  # Replace with actual verification
            st.session_state['captcha_verified'] = True
            st.experimental_rerun()
        else:
            st.error("reCAPTCHA verification failed. Please try again.")
    else:
        st.stop()
