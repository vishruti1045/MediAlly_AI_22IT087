import streamlit as st
from Home import home
from Login import login
from Register import register
from Prediction import prediction
from utils.utils import set_background

# Session state init
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "username" not in st.session_state:
    st.session_state["username"] = ""

def switch_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()

# # Background image
# try:
#     set_background("assets/home.jpg")
# except Exception as e:
#     st.error(f"⚠️ Background image not found: {e}")

# Custom Styles
st.markdown("""
<style>
/* Main App Styling */
.stApp {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f0f2f6;
}


/* Fix top bar / spacing */
/* Removes top padding/margin */
header, .block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}


/* Ensure navbar does not stretch or add white bar */
.navbar {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 1rem 2rem;
            position: fixed;
            top: 3.5rem;
            width: 100%;
            z-index: 999;
            display: flex;
            justify-content: flex-end; /* Align navbar content to the right */
            align-items: center;
            border-radius: 0 0 12px 12px;
            left: 0;
            right: 0;
        }}

            
.navbar .stButton > button {
    border: none;
    border-radius: 8px;
    background: #4f8bf9;
    color: white;
    font-weight: bold;
    padding: 8px 16px;
    cursor: pointer;
    transition: background 0.3s;
}
.navbar .stButton > button:hover {
    background: #3b73db;
}

/* Feature Cards */
.feature-card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    font-size: 16px;
    font-weight: 500;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

/* CTA Buttons */
.stButton > button {
    background-color: #4f8bf9;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;  /* Full width inside column */
    transition: all 0.3s ease-in-out;
}

.stButton > button:hover {
    background-color: #3b73db;
}

/* Container */
.main > div {
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 20px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

    /* Fix invisible input boxes */
/* Ensure input fields are visible */
input, textarea, .stTextInput input, .stTextArea textarea {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: #000 !important;
    border-radius: 10px !important;
    border: 1px solid #ccc !important;
    padding: 0.5rem !important;
}

input:focus, textarea:focus {
    outline: none !important;
    border: 2px solid #4f8bf9 !important;
}


</style>
""", unsafe_allow_html=True)

# ✅ Navigation Bar
st.markdown('<div class="navbar">', unsafe_allow_html=True)
nav1, nav2, nav3, nav_spacer, user_col = st.columns([1, 1, 1, 4, 2])

# with nav1:
#     if st.button("🏠 Home", key="home_btn"):
#         switch_page("home")

# with nav2:
#     if st.button("🧠 Prediction", key="prediction_btn"):
#         switch_page("prediction")

# with nav3:
#     if not st.session_state["logged_in"]:
#         if st.button("🔓 Login", key="login_nav_btn"):
#             switch_page("login")

with user_col:
    if st.session_state["logged_in"]:
        st.write(f"👤 {st.session_state.get('username', 'User')}")
        if st.button("🔴 Logout", key="logout_btn"):
            st.session_state.clear()
            switch_page("home")

st.markdown('</div>', unsafe_allow_html=True)

# Page Router
page_mapping = {
    "home": home,
    "login": login,
    "register": register,
    "prediction": prediction,
}
if st.session_state["page"] in page_mapping:
    with st.container():
        page_mapping[st.session_state["page"]](switch_page)
