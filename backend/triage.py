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
    disease = disease.strip().lower()

    # Fuzzy match to disease_risk_scores
    possible_match = get_close_matches(disease, [d.lower() for d in disease_risk_scores.keys()], n=1, cutoff=0.6)
    if possible_match:
        matched = next((d for d in disease_risk_scores if d.lower() == possible_match[0]), None)
        risk_score = disease_risk_scores.get(matched, 3)
    else:
        risk_score = 3  # default risk

    # Determine triage level
    if risk_score >= 7:
        return "🔴 Red (Emergency)"
    elif 4 <= risk_score <= 6:
        return "🟡 Yellow (Doctor Visit)"
    elif confidence < 0.10:
        return "🟢 Green (Uncertain - Home Care)"
    else:
        return "🟢 Green (Home Care)"
