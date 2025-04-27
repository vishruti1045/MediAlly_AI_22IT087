import streamlit as st
import base64
import os

def get_base64_of_image(image_path):
    """Encodes an image in Base64 for setting as a background."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def set_background(image_file_path):
    if not os.path.exists(image_file_path):
        st.warning("⚠️ Background image not found.")
        return
    
    with open(image_file_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def apply_custom_styles():
    st.markdown("""
        <style>
            .container {
                text-align: center;
                padding: 2rem;
                animation: fadeIn 1s ease-in;
            }
            .title p {
                font-size: 18px;
                color: #eee;
            }
            .features-row {
                display: flex;
                justify-content: center;
                gap: 1rem;
                flex-wrap: wrap;
                margin-top: 2rem;
            }
            .feature-card {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 15px;
                width: 280px;
                color: white;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: transform 0.3s ease, background 0.3s ease;
            }
            .feature-card:hover {
                background-color: rgba(255, 255, 255, 0.2);
                transform: translateY(-5px);
            }
            .cta-row {
                margin-top: 2.5rem;
                display: flex;
                justify-content: center;
                gap: 1.5rem;
                flex-wrap: wrap;
            }
            .cta-button {
                background: linear-gradient(to right, #06beb6, #48b1bf);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 10px;
                font-size: 1rem;
                cursor: pointer;
                transition: background 0.3s ease, transform 0.3s ease;
            }
            .cta-button:hover {
                background: linear-gradient(to right, #43cea2, #185a9d);
                transform: scale(1.05);
            }
            .fade-in {
                animation: fadeIn 1.2s ease forwards;
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)