import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def login(switch_page):
    st.subheader("🔑 Login to Your Account")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login"):
        if not username or not password:
            st.warning("⚠️ Please enter both username and password.")
        else:
            try:
                response = requests.post(API_URL + "/login", json={"username": username, "password": password})
                st.write("Response Status Code:", response.status_code)
                st.write("Response Text:", response.text)  # Print response content

                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Successfully logged in!")
                    switch_page("Prediction")
                else:
                    try:
                        error_msg = response.json().get("error", "Login failed.")  # Try parsing JSON
                    except requests.exceptions.JSONDecodeError:
                        error_msg = "Server did not return JSON. Check backend logs."
                    st.error(f"❌ {error_msg}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Unable to connect to backend.")
