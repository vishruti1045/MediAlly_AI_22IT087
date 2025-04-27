import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"


def switch_page(page_name):
    """Function to switch pages using session state."""
    st.session_state["current_page"] = page_name
    st.rerun()  # Refresh the UI
    
def register(switch_page):
    st.title("📝 Register Page")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and email and password:
            response = requests.post(f"{API_URL}/register", json={
                "username": username,
                "email": email,
                "password": password
            })

            if response.status_code == 200:
                st.success("✅ Registration successful! Please login.")
                switch_page("login")
            else:
                try:
                    error_msg = response.json().get('error', 'Unknown error')
                except requests.exceptions.JSONDecodeError:
                    error_msg = response.text  # fallback to raw text if not JSON

                st.error(f"❌ Error: {error_msg}")
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")
