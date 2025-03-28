import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def login(switch_page=None):
    st.subheader("🔐 Login to Your Account")
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🔓 Login"):
        response = requests.post(f"{API_URL}/login", json={
            "username": username, "password": password
        })
        result = response.json()

        if response.status_code == 200:
            st.success("✅ OTP sent to email and phone! Verify to proceed.")
            st.session_state["username"] = username
            switch_page("verify_login_otp")
        else:
            st.error(f"❌ {result.get('error', 'Login failed')}")

def verify_login_otp(switch_page=None):
    st.subheader("🔑 Verify Login OTP")
    
    otp_email = st.text_input("📧 Enter Email OTP")
    otp_phone = st.text_input("📱 Enter Mobile OTP")

    if st.button("✅ Verify & Login"):
        response = requests.post(f"{API_URL}/verify_login_otp", json={
            "username": st.session_state["username"], "otp_email": otp_email, "otp_phone": otp_phone
        })
        result = response.json()

        if response.status_code == 200:
            st.session_state["logged_in"] = True
            st.success("🎉 Login successful!")
            switch_page("prediction")  # Redirect to the prediction page
        else:
            st.error(f"❌ {result.get('error', 'OTP verification failed')}")