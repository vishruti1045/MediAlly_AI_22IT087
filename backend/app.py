from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from pymongo import MongoClient
from werkzeug.security import check_password_hash


# Initialize Flask app
app = Flask(__name__)
CORS(app)


load_dotenv()  # Ensure .env file is loaded

# Fetch MongoDB URI from .env file
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("❌ MONGO_URI not found in .env file!")
else:
    print(f"✅ MongoDB URI loaded: {mongo_uri[:30]}...")  # Print first 30 chars


#client.get_database() Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set MongoDB URI
client = MongoClient(mongo_uri)
mongo = client["medially"]  # Ensure you specify the correct database name

# Check MongoDB connection
try:
    mongo.command("ping")  # Corrected method
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")



# Load BioBERT Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
biobert_model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1").to(device)

# Symptom Classification Model
class SymptomClassifier(torch.nn.Module):
    def __init__(self, input_size, num_classes):
        super(SymptomClassifier, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 128)
        self.bn1 = torch.nn.BatchNorm1d(128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.bn2 = torch.nn.BatchNorm1d(64)
        self.fc3 = torch.nn.Linear(64, 24)  # Match saved model's output size

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.fc3(x)
        return x


# Load trained classification model
num_classes = 10
MODEL_PATH = os.getenv("MODEL_PATH", r"C:\MediAlly_AI\medially.pth")

if os.path.exists(MODEL_PATH):
    symptom_model = SymptomClassifier(input_size=768, num_classes=num_classes).to(device)
    symptom_model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    symptom_model.eval()
    print("✅ Symptom Classification Model Loaded!")
else:
    print(f"❌ Model file not found at {MODEL_PATH}")
    symptom_model = None  # Prevent errors if model is missing

# Label Encoder
label_encoder = {i: f"Disease {i}" for i in range(num_classes)}

# API: User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({"message": "Send a POST request with username and password"}), 200
    
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if mongo.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    mongo.users.insert_one({
        "username": username,
        "password": generate_password_hash(password)
    })
    return jsonify({"message": "Registration successful"}), 201

# API: User Login
@app.route("/login", methods=["POST"])  # Ensure only POST is allowed
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "jack" and password == "sparrow":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to MediAlly API!"}), 200


# API: Predict Disease
@app.route("/predict", methods=["POST"])
def predict():
    if symptom_model is None:
        return jsonify({"error": "Model is not loaded"}), 500

    data = request.json
    text = data.get("symptoms", "").strip()

    if not text:
        return jsonify({"error": "No symptoms provided"}), 400

    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)

    with torch.no_grad():
        embeddings = biobert_model(**tokens).last_hidden_state[:, 0, :]
        output = symptom_model(embeddings)
        probabilities = F.softmax(output, dim=1)

    top_probs, top_classes = torch.topk(probabilities, 3)
    predictions = [(label_encoder[top_classes[0][i].item()], top_probs[0][i].item()) for i in range(3)]

    return jsonify({
        "predicted_disease": predictions[0][0],
        "confidence": float(predictions[0][1]),
        "top_predictions": predictions
    })

if __name__ == "__main__":
    app.run(debug=True)
