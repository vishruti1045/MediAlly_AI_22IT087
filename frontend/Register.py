import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def register(switch_page=None):
    st.subheader("📝 Register a New Account")
    
    username = st.text_input("👤 Choose a Username")
    password = st.text_input("🔒 Choose a Password", type="password")
    email = st.text_input("📧 Enter Your Email")
    phone = st.text_input("📱 Enter Your Mobile Number")

    if st.button("📝 Register"):
        if username and password and email and phone:
            response = requests.post(f"{API_URL}/register", json={
                "username": username, "password": password, "email": email, "phone": phone
            })
            result = response.json()

            if response.status_code == 201:
                st.success("✅ OTP sent! Verify your account.")
                st.session_state["username"] = username
                switch_page("verify_register_otp")
            else:
                st.error(f"❌ {result.get('error', 'Registration failed')}")

def verify_register_otp(switch_page=None):
    st.subheader("🔑 Verify Registration OTP")
    
    otp_email = st.text_input("📧 Enter Email OTP")
    
    if st.button("✅ Verify"):
        response = requests.post(f"{API_URL}/verify_register_otp", json={
            "username": st.session_state["username"], "otp_email": otp_email
        })
        result = response.json()

        if response.status_code == 200:
            st.success("🎉 Account verified! You can now log in.")
            switch_page("login")
        else:
            st.error(f"❌ {result.get('error', 'OTP verification failed')}")
