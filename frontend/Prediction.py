import streamlit as st
import requests
from utils.utils import set_background
import logging
import base64

API_URL = "http://127.0.0.1:5000"

# Function to convert image to base64
def get_base64_from_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    file_handler = logging.FileHandler('prediction.log')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def prediction(switch_page):
    # Set background image
    bg_base64 = get_base64_from_image("C:/MediAlly_AI/frontend/assets/bot.jpg")
    st.markdown(f"""
    <style>
        .stApp {{
            background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed;
            background-size: cover;
        }}
        .glass-prediction {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 5rem auto;
            max-width: 800px;
            color: #ffffff;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: fadeIn 1s ease;
        }}
        textarea, .stTextInput>div>div>input {{
            background: rgba(255,255,255,0.4) !important;
            border-radius: 12px !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            color: #000000 !important;
        }}
        .stButton>button {{
            background-color: #4A90E2;
            color: white;
            padding: 0.6rem 2rem;
            font-size: 1rem;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            margin-top: 1rem;
            transition: all 0.3s ease-in-out;
        }}
        .stButton>button:hover {{
            background-color: #357ABD;
            transform: scale(1.05);
            cursor: pointer;
        }}
        @keyframes fadeIn {{
            from {{opacity: 0; transform: translateY(20px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}
        h3 {{
            text-align: center;
            color: #fff;
            font-weight: bold;
        }}
        label {{
            font-weight: 500;
            color: #ffffff;
        }}
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.get("logged_in", False):
        st.warning("⚠️ Please log in first!")
        logger.warning("User not logged in")
        return

    # 🔲 Start glass container
    st.markdown('<div class="glass-prediction">', unsafe_allow_html=True)

    st.subheader("🩺 Medical Symptom Assistant")
    symptoms = st.text_area("💬 Describe your symptoms...")

    if st.button("Predict"):
        if not symptoms.strip():
            st.warning("⚠️ Please enter symptoms.")
            logger.warning("No symptoms entered")
        else:
            with st.spinner("🔍 Analyzing symptoms..."):
                try:
                    response = requests.post(f"{API_URL}/predict", json={"symptoms": symptoms})
                    response.raise_for_status()
                    result = response.json()

                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                        logger.error(f"Error: {result['error']}")
                    else:
                        predicted_disease = result.get("predicted_disease", "Unknown")
                        confidence = result.get("confidence", 0.0)
                        triage_category = result.get("triage_category", "Unknown")
                        top_predictions = result.get("top_predictions", [])

                        diseases, confidences, icd_codes = [], [], []

                        for item in top_predictions:
                            if isinstance(item, dict):
                                diseases.append(item.get("disease", "Unknown"))
                                confidences.append(item.get("confidence", 0.0))
                                icd_codes.append(item.get("icd_code", "N/A"))
                            elif isinstance(item, list) and len(item) == 2:
                                diseases.append(item[0])
                                confidences.append(item[1])
                                icd_codes.append("N/A")
                            else:
                                st.warning(f"⚠️ Unexpected data format: {item}")
                                logger.warning(f"Unexpected data format: {item}")

                        triage_map = {
                            "Red": "🔴 Red (Emergency)",
                            "Orange": "🟠 Orange (Urgent)",
                            "Yellow": "🟡 Yellow (Doctor Visit)",
                            "Green": "🟢 Green (Home Care)",
                            "Blue": "🔵 Unknown"
                        }
                        triage_display = triage_map.get(triage_category, "🔵 Unknown")

                        if diseases:
                            st.markdown(f"""
                            🔍 **Predicted Disease:** Possible Conditions: {", ".join(diseases[:3])}  
                            🎯 **Confidence:** {max(confidences[:3]) * 100:.0f}%  
                            🚑 **Triage Category:** {triage_display}  
                            📌 **ICD-10 Code(s):** {', '.join([f"{code} ({d})" for code, d in zip(icd_codes[:3], diseases[:3])])}
                            """)
                        else:
                            st.warning("⚠️ No predictions available.")
                            logger.warning("No predictions returned")

                except requests.exceptions.RequestException as err:
                    st.error(f"❌ Server error: {err}")
                    logger.error(f"Server error: {err}")

    # 🔲 End glass container
    st.markdown('</div>', unsafe_allow_html=True)

