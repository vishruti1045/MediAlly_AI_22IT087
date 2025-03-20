import streamlit as st

def logout():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.success("🔴 You have been logged out!")
    else:
        st.warning("⚠️ You are not logged in.")
