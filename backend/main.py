from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModel
import joblib

from model import symptom_model  # Ensure model.py is correctly set up
from triage import triage_category

# Initialize Flask app
app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# ✅ Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ MONGO_URI not found in .env file!")
    exit(1)

# ✅ Connect to MongoDB
client = MongoClient(mongo_uri)
mongo_db = client["medially"]
users_collection = mongo_db["users"]

try:
    mongo_db.command("ping")
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    exit(1)

# ✅ Load Label Encoder
try:
    label_encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    print("❌ label_encoder.pkl not found!")
    label_encoder = None

# ✅ Load BioBERT
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
biobert_model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1").to(device)

def get_bert_embedding(text_list):
    """Encodes input text into BioBERT embeddings."""
    tokens = tokenizer(text_list, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        embeddings = biobert_model(**tokens).last_hidden_state[:, 0, :]
    return embeddings

# ✅ User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "Registration successful"}), 201

# ✅ User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if user and bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ✅ Symptom Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    if symptom_model is None:
        return jsonify({"error": "Model is not loaded"}), 500

    if label_encoder is None:
        return jsonify({"error": "Label encoder is not loaded"}), 500

    data = request.json
    text = data.get("symptoms", "").strip()

    if not text:
        return jsonify({"error": "No symptoms provided"}), 400

    embedding = get_bert_embedding([text])  # Make sure this function works!

    with torch.no_grad():
        output = symptom_model(embedding)
        probabilities = torch.nn.functional.softmax(output, dim=1)

    top_probs, top_classes = torch.topk(probabilities, 3)
    predictions = [(label_encoder.inverse_transform([top_classes[0][i].item()])[0], top_probs[0][i].item()) for i in range(3)]

    return jsonify({
        "predicted_disease": predictions[0][0],
        "confidence": float(predictions[0][1]),
        "top_predictions": predictions
    })


# ✅ Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to MediAlly API!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
