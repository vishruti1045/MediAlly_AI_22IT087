import streamlit as st
import requests
import os
import base64

# API URL
API_URL = "http://127.0.0.1:5000"

image_path="/assets/home-back.jpg"
# Function to encode an image in Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Function to set the background image
def set_background(image_path):
    if os.path.exists(image_path):
        image_base64 = get_base64_of_image(image_path)
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{image_base64}");
                    background-size: cover;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Function to display the home page
def home(switch_page=None):  # ✅ Accept switch_page as an optional argument
    st.title("🏠 MediAlly - Medical Symptom Assistant")
    st.write("🔍 AI-powered disease prediction from symptoms.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Login"):
            if switch_page:
                switch_page("login")
            else:
                st.session_state["page"] = "login"
    with col2:
        if st.button("📝 Register"):
            if switch_page:
                switch_page("register")
            else:
                st.session_state["page"] = "register"

