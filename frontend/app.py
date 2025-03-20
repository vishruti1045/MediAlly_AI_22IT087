import streamlit as st

st.set_page_config(page_title="MediAlly - Symptom Assistant", page_icon="🩺", layout="wide")

st.sidebar.title("🔍 MediAlly Navigation")

# Navigation Menu
page = st.sidebar.radio("Go to", ["Home", "Login", "Register", "Prediction", "Logout"])

# Redirect to selected page
if page == "Home":
    from Home import home
    home()
elif page == "Login":
    from Login import login
    login()
elif page == "Register":
    from Register import register
    register()
elif page == "Prediction":
    from Prediction import prediction
    prediction()
elif page == "Logout":
    from Logout import logout
    logout()
