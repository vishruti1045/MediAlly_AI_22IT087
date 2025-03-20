import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def prediction():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in first!")
        return

    st.subheader("📝 Describe Your Symptoms")

    symptoms = st.text_area("💬 Type your symptoms here...", height=150)

    if st.button("🔍 Predict Disease"):
        if symptoms:
            with st.spinner("⏳ Analyzing symptoms..."):
                try:
                    response = requests.post(API_URL + "/predict", json={"symptoms": symptoms})

                    if response.status_code == 200:
                        result = response.json()

                        # Extracting Data
                        predicted_disease = result.get('predicted_disease', 'N/A')
                        confidence = result.get('confidence', 0)
                        icd_code = result.get('icd_code', 'Unknown')
                        triage_category = result.get('triage_category', 'Unknown')

                        triage_emojis = {
                            "Green": "🟢 Green (Home Care)",
                            "Yellow": "🟡 Yellow (Doctor Visit Recommended)",
                            "Red": "🔴 Red (Emergency - Immediate Attention Required)"
                        }
                        triage_display = triage_emojis.get(triage_category, "Unknown")

                        # Display structured output
                        st.markdown(f"""
                        ### 📌 ICD-10 Code for {predicted_disease}: **{icd_code}**

                        🔍 **Predicted Disease:** {predicted_disease}  
                        🎯 **Confidence:** {confidence:.2%}  
                        🚑 **Triage Category:** {triage_display}

                        ### 📌 Top Predictions:
                        """)

                        for disease, prob in result.get("top_predictions", []):
                            st.markdown(f"✔️ **{disease}**: {prob:.2%}")

                    else:
                        st.error(f"❌ Prediction failed! (Error {response.status_code})")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Unable to connect to the backend.")

        else:
            st.warning("⚠️ Please enter your symptoms to proceed.")
