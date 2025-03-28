import streamlit as st
import requests
import os
import base64

# ✅ Function to convert image to Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# ✅ Function to set background image
def set_background(image_path):
    if os.path.exists(image_path):
        image_base64 = get_base64_of_image(image_path)
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{image_base64}");
                    background-size: cover;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

# ✅ API URL
API_URL = "http://127.0.0.1:5000"

# ✅ Prediction Function
def prediction():
    if not st.session_state.get("logged_in", False):
        st.warning("⚠️ Please log in first!")
        return

    set_background("assets/prediction-back.jpg")
    st.subheader("🩺 Medical Symptom Assistant")
    
    symptoms = st.text_area("💬 Describe your symptoms...")

    if st.button("Predict"):
        if not symptoms.strip():
            st.warning("⚠️ Please enter symptoms.")
            return

        with st.spinner("🔍 Analyzing symptoms..."):
            try:
                response = requests.post(f"{API_URL}/predict", json={"symptoms": symptoms})
                response.raise_for_status()  # 🚨 Catch HTTP errors
                
                # ✅ Validate API response format
                result = response.json()
                if "error" in result:
                    st.error(f"❌ {result['error']}")
                    return

                # ✅ Extract data from API response
                predicted_disease = result.get("predicted_disease", "Unknown")
                confidence = result.get("confidence", 0.0)
                top_predictions = result.get("top_predictions", [])

                # ✅ Display results
                st.success(f"🎯 **Predicted Disease:** {predicted_disease} ({confidence * 100:.2f}%)")
                st.write("### 🔍 Top Predicted Diseases:")
                
                if top_predictions:
                    # Convert to table format
                    pred_table = [{"Disease": disease, "Confidence (%)": f"{conf * 100:.2f}%"} for disease, conf in top_predictions]
                    st.table(pred_table)
                else:
                    st.warning("⚠️ No predictions available.")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to API. Is the Flask server running?")
            except requests.exceptions.HTTPError as errh:
                st.error(f"❌ HTTP Error: {errh}")
            except requests.exceptions.RequestException as err:
                st.error(f"❌ Server error: {err}")
