import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

def prediction():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in first!")
        return

    st.subheader("📝 Describe Your Symptoms")

    # ✅ Add a unique key to avoid duplicate element errors
    symptoms = st.text_area("💬 Type your symptoms here...", height=150, key="symptom_input")

    if st.button("Predict"):
        if not symptoms.strip():
            st.warning("⚠️ Please enter your symptoms to proceed.")
            return
        
        try:
            response = requests.post(f"{API_URL}/predict", json={"symptoms": symptoms})

            # Debugging API response
            st.write(f"🔄 **Debugging:** API Status Code: {response.status_code}")
            st.write(f"🔄 **Debugging:** API Response: {response.text}")

            if response.status_code == 200:
                result = response.json()
                st.write(f"🔍 **Predicted Disease:** {result['predicted_disease']}")
                st.write(f"🎯 **Confidence:** {result['confidence']:.2%}")
                st.write(f"🚑 **Triage Category:** {result.get('triage', 'N/A')}")
            else:
                st.error("❌ Error: Failed to get prediction. Please try again.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Server error: {e}")

# Run prediction function when Streamlit app starts
prediction()
