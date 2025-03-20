import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def register():
    st.subheader("📝 Register for an Account")

    username = st.text_input("👤 Choose a Username")
    password = st.text_input("🔒 Choose a Password", type="password")

    if st.button("📝 Register"):
        if not username or not password:
            st.warning("⚠️ Please enter both username and password.")
        else:
            try:
                response = requests.post(API_URL + "/register", json={"username": username, "password": password})
                
                if response.status_code == 201:
                    st.success("✅ Registration successful! You can now log in.")
                else:
                    error_msg = response.json().get("error", "Registration failed.")
                    st.error(f"❌ {error_msg}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Unable to connect to backend.")
