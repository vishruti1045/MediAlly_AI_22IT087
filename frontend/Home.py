import streamlit as st

def home():
    st.markdown("<h1 style='text-align: center;'>🩺 MediAlly - Medical Symptom Assistant</h1>", unsafe_allow_html=True)
    st.write("🔍 Enter your symptoms to get AI-powered disease predictions.")
    
    st.image("https://cdn-icons-png.flaticon.com/512/3077/3077034.png", width=250, use_column_width=True)

    st.write("🚀 Get started by navigating to Login or Register!")
