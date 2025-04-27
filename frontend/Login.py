import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def login(switch_page):
    st.title("🔐 Login")

    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False

    if not st.session_state["otp_sent"]:
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            if username and password:
                response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                result = response.json()

                if response.status_code == 200:
                    st.session_state["username"] = username
                    st.session_state["otp_sent"] = True  # ✅ Show OTP input
                    st.success("📨 OTP sent to your email. Enter OTP below to continue.")
                else:
                    st.error(f"❌ {result.get('error', 'Login failed')}")
            else:
                st.warning("⚠️ Please enter both username and password.")

    if st.session_state["otp_sent"]:
        otp = st.text_input("🔢 Enter OTP")
        if st.button("Verify OTP"):
            verify_otp(otp, switch_page)

def verify_otp(otp, switch_page):
    if not otp:
        st.warning("⚠️ Please enter the OTP.")
        return

    response = requests.post(f"{API_URL}/verify_login_otp", json={"username": st.session_state["username"], "otp_email": otp})
    result = response.json()

    if response.status_code == 200:
        st.session_state["logged_in"] = True
        st.success("🎉 Login successful! Redirecting to Prediction...")
        switch_page("prediction")  
    else:
        st.error(f"❌ {result.get('error', 'OTP verification failed')}")
