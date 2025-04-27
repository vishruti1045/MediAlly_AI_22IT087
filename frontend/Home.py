import streamlit as st
import base64

def home(switch_page):
    img_path = "C:/MediAlly_AI/frontend/assets/pred.jpg"
    with open(img_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    # Custom HTML & CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
            padding-top: 6rem;
        }}

        .navbar {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 1rem 2rem;
            position: fixed;
            top: 3.5rem;
            width: 100%;
            z-index: 999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 0 0 12px 12px;
            left: 0;
            right: 0;
        }}

        .navbar-left a {{
            margin: 0 1.2rem;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 1rem;
        }}

        .navbar-left a:hover {{
            color: #4A90E2;
        }}

        .glass {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 3rem 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            margin: 3rem auto;
            max-width: 900px;
            color: white;
            text-align: center;
        }}

        .features {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 2rem;
            margin-top: 2rem;
        }}

        .feature-card {{
            background-color: rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 1.5rem;
            width: 250px;
            backdrop-filter: blur(8px);
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.2);
            color: white;
            transition: transform 0.3s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-10px);
        }}

        .auth-button button {{
            width: 140px;
            padding: 0.6rem 1rem;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            background-color: #4f8bf9;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .auth-button button:hover {{
            background-color: #3b73db;
        }}
    </style>

    <div class="navbar">
        <div class="navbar-left">
            <a href="#hero">Home</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="glass" id="hero">
            <h1 style="font-size: 3rem;">Welcome to MediAlly</h1>
            <p style="font-size: 1.3rem; max-width: 700px; margin: auto;">
                Introducing our AI-powered Medical Symptom Assistant — a tool designed to assess symptoms, predict possible conditions, categorize risk levels, and provide ICD-10 codes for better understanding your health. <br>This AI assistant leverages cutting-edge Natural Language Processing (NLP) models to offer reliable symptom analysis.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Login/Register Buttons under Welcome
    if not st.session_state.get("logged_in"):
        st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
        col1, col2, _ = st.columns([1, 1, 2])
        with col1:
            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("🔓 Login"):
                switch_page("login")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="auth-button">', unsafe_allow_html=True)
            if st.button("📝 Register"):
                switch_page("register")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div class="glass" id="features">
            <h2>Key Features</h2>
            <div class="features">
                <div class="feature-card">🩺<br><b>AI Diagnosis</b><br>Instant predictions based on symptoms.</div>
                <div class="feature-card">📊<br><b>Health Insights</b><br>Personalized suggestions.</div>
                <div class="feature-card">🔒<br><b>Secure Data</b><br>Your data stays encrypted and safe.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # About Section
    # About Section
    st.markdown("""
    <div class="glass" id="about">
        <h2>About MediAlly</h2>
        <p style="max-width: 800px; margin: auto; font-size: 1.1rem;">
            MediAlly simplifies the medical diagnosis process using <b>AI</b>. It evaluates symptoms and delivers
            personalized insights while keeping your data private.
            <br><br>
            Ensuring reliability is our top priority. Our model has been evaluated on real-world medical datasets and achieves:
        </p>
        <ul style="text-align: left; max-width: 800px; margin: 1rem auto; font-size: 1.05rem; line-height: 1.6;">
            <li>✅ <b>Overall Accuracy:</b> ~85% on test data</li>
            <li>✅ <b>Precision & Recall:</b> Optimized for high recall to avoid missing serious conditions</li>
            <li>✅ <b>False Negatives:</b> Minimized to prevent misclassification of severe conditions</li>
        </ul>
    </div>
""", unsafe_allow_html=True)


    # Contact Section
    st.markdown("""
        <div class="glass" id="contact">
            <h2>Contact Us</h2>
            <p style="max-width: 800px; margin: auto;">
                Got questions or feedback? Reach out to us at 
                <a href="mailto:support@medially.ai" style="color: #4A90E2;">support@medially.ai</a>.
            </p>
        </div>
    """, unsafe_allow_html=True)
