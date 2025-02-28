import streamlit as st
from PIL import Image

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            max-width: 800px;
            padding: 2rem;
        }
        .login-box {
            background-color: #f8f9fa;
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-top: 2rem;
        }
        .provider-button {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .provider-button:hover {
            transform: translateY(-2px);
        }
        .logo-container {
            text-align: center;
            margin-bottom: 3rem;
        }
        .title {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 2rem;
        }
        .divider {
            text-align: center;
            margin: 2rem 0;
            color: #7f8c8d;
        }
    </style>
""", unsafe_allow_html=True)

# Display logo
logo = Image.open("shaped-ai.png")
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image(logo, width=300, use_column_width='auto')
st.markdown('</div>', unsafe_allow_html=True)

# Check authentication status
if not st.experimental_user.is_logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">Secure Access Portal</h1>', unsafe_allow_html=True)
    
    # Login options grid
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🚀 **Google Workspace**\n\nSign in with your Google account",
            key="google",
            help="Login using Google Identity"
        ):
            st.login("google")
        
        st.markdown('<div class="divider">───── or ─────</div>', unsafe_allow_html=True)
        
        if st.button(
            "🔐 **Auth0**\n\nEnterprise authentication",
            key="auth0",
            help="Login using Auth0"
        ):
            st.login("auth0")

    with col2:
        if st.button(
            "🏢 **Microsoft Entra**\n\nCompany Azure AD account",
            key="microsoft",
            help="Login using Microsoft Entra ID"
        ):
            st.login("microsoft")
        
        st.markdown('<div class="divider">───── or ─────</div>', unsafe_allow_html=True)
        
        if st.button(
            "🛡️ **Okta**\n\nSSO & Identity management",
            key="okta",
            help="Login using Okta"
        ):
            st.login("okta")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #7f8c8d;">
            🔒 Your security is our priority. All logins are encrypted.
        </div>
    """, unsafe_allow_html=True)
else:
    # User is logged in - show dashboard
    st.success(f"🌟 Welcome back, {st.experimental_user.name}!")
    with st.expander("👤 Account Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {st.experimental_user.name}")
            st.write(f"**Email:** {st.experimental_user.email}")
        with col2:
            st.write("**Last Login:** Just now")
            st.write("**Account Status:** ✅ Active")
    
    if st.button("🚪 Logout", type="primary"):
        st.logout()
        st.experimental_rerun()
