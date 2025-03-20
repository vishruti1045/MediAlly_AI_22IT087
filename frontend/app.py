import streamlit as st

st.set_page_config(page_title="MediAlly - Symptom Assistant", page_icon="🩺", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Function to change pages
def switch_page(page):
    st.session_state.page = page
    st.rerun()

# Sidebar Navigation
st.sidebar.title("🔍 MediAlly Navigation")
if st.session_state.logged_in:
    st.sidebar.write(f"👋 Welcome, **{st.session_state.username}**")
    # if st.sidebar.button("🔴 Logout", key="logout_button"):

    #     st.session_state.logged_in = False
    #     st.session_state.username = None
    #     switch_page("Home")
else:
    st.sidebar.write("🚀 Please login or register to continue.")
    
# Page Routing
if st.session_state.page == "Home":
    from Home import home
    home(switch_page)
elif st.session_state.page == "Login":
    from Login import login
    login(switch_page)
elif st.session_state.page == "Register":
    from Register import register
    register(switch_page)
elif st.session_state.page == "Prediction":
    from Prediction import prediction
    prediction()
