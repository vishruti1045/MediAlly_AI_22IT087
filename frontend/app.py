import streamlit as st
from Home import home
from Login import login
from Register import register
from Prediction import prediction

# ✅ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ✅ Sidebar Navigation
st.sidebar.title("🔍 MediAlly Navigation")

if st.session_state["logged_in"]:
    st.sidebar.success(f"👋 Welcome, **{st.session_state.get('username', 'User')}**")

    if st.sidebar.button("🔴 Logout"):
        st.session_state.clear()
        st.session_state["logged_in"] = False
        st.rerun()
else:
    page = st.sidebar.radio("Navigation", ["Home", "Login", "Register"])
    st.session_state["page"] = page.lower()

# ✅ Page Routing
if st.session_state["page"] == "home":
    home()
elif st.session_state["page"] == "login":
    login()
elif st.session_state["page"] == "register":
    register()
elif st.session_state["page"] == "prediction":
    prediction()
