import streamlit as st

def home(switch_page):
    st.markdown("<h1 style='text-align: center;'>🩺 MediAlly - Medical Symptom Assistant</h1>", unsafe_allow_html=True)
    st.write("🔍 AI-powered disease prediction from symptoms.")

    st.image("https://cdn-icons-png.flaticon.com/512/3077/3077034.png", width=250)

    st.write("🚀 Get started by logging in or registering.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Login", key="login_button"):
            switch_page("Login")

    with col2:
        if st.button("📝 Register", key="register_button"):
            switch_page("Register")
