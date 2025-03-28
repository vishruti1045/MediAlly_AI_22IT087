from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import os
import random
import logging
from dotenv import load_dotenv
from twilio.rest import Client
from datetime import datetime, timedelta

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# ✅ MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
mongo_db = client["medially"]
users_collection = mongo_db["users"]
otps_collection = mongo_db["otps"]

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Email Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")
mail = Mail(app)

# ✅ Twilio Configuration
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# ✅ Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Send Email OTP
def send_email_otp(email, otp):
    try:
        msg = Message("Your OTP for MediAlly", sender=app.config["MAIL_USERNAME"], recipients=[email])
        msg.body = f"Your OTP is: {otp}. It expires in 5 minutes."
        mail.send(msg)
        return True
    except Exception as e:
        logging.error(f"❌ Email OTP Error for {email}: {e}")
        return False

# ✅ Send SMS OTP
def send_sms_otp(phone, otp):
    try:
        twilio_client.messages.create(body=f"Your MediAlly OTP is {otp}", from_=TWILIO_PHONE, to=phone)
        return True
    except Exception as e:
        logging.error(f"❌ SMS OTP Error for {phone}: {e}")
        return False

# ✅ Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to MediAlly AI!"}), 200

# ✅ User Registration (Email OTP)
@app.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.json
        username = data.get("username").strip()
        password = data.get("password")
        email = data.get("email").strip().lower()
        phone = data.get("phone").strip()

        if not all([username, password, email, phone]):
            return jsonify({"error": "All fields are required"}), 400

        # Check if user already exists
        if users_collection.find_one({"$or": [{"username": username}, {"email": email}, {"phone": phone}]}):
            return jsonify({"error": "Username, Email, or Phone already registered"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Generate Email OTP
        otp_email = generate_otp()
        expiry_time = datetime.utcnow() + timedelta(minutes=5)

        email_sent = send_email_otp(email, otp_email)
        if not email_sent:
            return jsonify({"error": "Failed to send email OTP. Try again."}), 500

        # Store user & OTP
        users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "email": email,
            "phone": phone,
            "verified": False
        })
        otps_collection.insert_one({
            "username": username,
            "otp_email": otp_email,
            "expires_at": expiry_time,
            "purpose": "registration"
        })

        return jsonify({"message": "OTP sent to email. Verify your account."}), 201
    except Exception as e:
        logging.error(f"❌ Registration Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ✅ Verify Registration OTP
@app.route("/verify_register_otp", methods=["POST"])
def verify_register_otp():
    try:
        data = request.json
        username = data.get("username")
        otp_email = data.get("otp_email")

        user = users_collection.find_one({"username": username})
        otp_record = otps_collection.find_one({"username": username, "purpose": "registration"})

        if not user or not otp_record:
            return jsonify({"error": "User not found or OTP expired"}), 404

        # Check OTP expiry
        if datetime.utcnow() > otp_record["expires_at"]:
            return jsonify({"error": "OTP expired. Please request a new one."}), 400

        if otp_record["otp_email"] == otp_email:
            users_collection.update_one({"username": username}, {"$set": {"verified": True}})
            otps_collection.delete_one({"username": username, "purpose": "registration"})
            return jsonify({"message": "Account verified successfully!"}), 200
        else:
            return jsonify({"error": "Invalid OTP"}), 400
    except Exception as e:
        logging.error(f"❌ OTP Verification Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ✅ Login API with OTP Verification
@app.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        username = data.get("username").strip()
        password = data.get("password")

        user = users_collection.find_one({"username": username})

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not user.get("verified", False):
            return jsonify({"error": "Account not verified. Complete email verification first."}), 403

        if bcrypt.check_password_hash(user["password"], password):
            # Generate OTPs for login verification
            otp_email = generate_otp()
            otp_phone = generate_otp()
            expiry_time = datetime.utcnow() + timedelta(minutes=5)

            email_sent = send_email_otp(user["email"], otp_email)
            sms_sent = send_sms_otp(user["phone"], otp_phone)

            if not email_sent or not sms_sent:
                return jsonify({"error": "Failed to send OTPs. Try again."}), 500

            # Store login OTP
            otps_collection.insert_one({
                "username": username,
                "otp_email": otp_email,
                "otp_phone": otp_phone,
                "expires_at": expiry_time,
                "purpose": "login"
            })

            return jsonify({"message": "OTP sent to email & phone. Verify to login."}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logging.error(f"❌ Login Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ✅ Verify Login OTP
@app.route("/verify_login_otp", methods=["POST"])
def verify_login_otp():
    try:
        data = request.json
        username = data.get("username")
        otp_email = data.get("otp_email")
        otp_phone = data.get("otp_phone")

        otp_record = otps_collection.find_one({"username": username, "purpose": "login"})

        if not otp_record:
            return jsonify({"error": "OTP expired or invalid"}), 400

        # Check OTP expiry
        if datetime.utcnow() > otp_record["expires_at"]:
            return jsonify({"error": "OTP expired. Please login again."}), 400

        if otp_record["otp_email"] == otp_email and otp_record["otp_phone"] == otp_phone:
            otps_collection.delete_one({"username": username, "purpose": "login"})
            return jsonify({"message": "Login verified successfully!"}), 200
        else:
            return jsonify({"error": "Invalid OTP"}), 400
    except Exception as e:
        logging.error(f"❌ OTP Login Verification Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
