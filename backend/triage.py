import requests
from difflib import get_close_matches

# ✅ Disease Risk Scores for triage
disease_risk_scores = {
    "Psoriasis": 3, "Varicose Veins": 3, "Peptic Ulcer Disease": 5,
    "Drug Reaction": 6, "Gastroesophageal Reflux Disease": 4,
    "Allergy": 3, "Urinary Tract Infection": 5, "Malaria": 7,
    "Jaundice": 6, "Cervical Spondylosis": 4, "Migraine": 4,
    "Hypertension": 5, "Bronchial Asthma": 7, "Acne": 2,
    "Arthritis": 4, "Dimorphic Hemorrhoids": 3, "Pneumonia": 8,
    "Common Cold": 2, "Fungal Infection": 3, "Dengue": 8,
    "Impetigo": 3, "Chicken Pox": 4, "Typhoid": 7, "Diabetes": 6,
}

# ✅ Local ICD-10 mappings
local_icd10 = {
    "dengue": "A90",
    "dengue fever": "A90",
    "malaria": "B50",
    "typhoid": "A01.0",
    "typhoid fever": "A01.0",
    "pneumonia": "J18.9",
    "chicken pox": "B01",
    "varicella": "B01",
    "fungal infection": "B35-B49",
    "mycosis": "B35-B49"
}

# ✅ ICD-10 Code Lookup with fallback
def get_icd10_code(disease):
    try:
        # Try external ICD API first
        url = f"https://icd.who.int/api/{disease.replace(' ', '%20')}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("icd10", "Unknown")
    except:
        pass

    # Fuzzy match local fallback
    disease = disease.strip().lower()
    possible_match = get_close_matches(disease, local_icd10.keys(), n=1, cutoff=0.6)
    if possible_match:
        return local_icd10.get(possible_match[0], "Unknown")
    return "Unknown"

# ✅ Triage Risk Category Function
def triage_category(disease, confidence):
    # Clean up the disease name
    disease = disease.strip().lower()

    # Fuzzy match to disease_risk_scores
    possible_match = get_close_matches(disease, [d.lower() for d in disease_risk_scores.keys()], n=1, cutoff=0.6)
    
    # Default risk score if no match found
    risk_score = 3  # default risk score

    if possible_match:
        matched = next((d for d in disease_risk_scores if d.lower() == possible_match[0]), None)
        risk_score = disease_risk_scores.get(matched, 3)

    # Ensure confidence is between 0 and 1 (just in case)
    if confidence < 0:
        confidence = 0
    elif confidence > 1:
        confidence = 1

    # Determine triage level based on risk score and confidence
    if risk_score >= 7 or confidence >= 0.8:
        return "🔴 Red (Emergency)"
    elif 4 <= risk_score <= 6 or confidence >= 0.5:
        return "🟠 Orange (Urgent)"
    elif 0.2 <= confidence < 0.5:
        return "🟡 Yellow (Doctor Visit)"
    else:
        return "🟢 Green (Home Care)"
