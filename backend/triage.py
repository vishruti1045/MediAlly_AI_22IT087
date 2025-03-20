# triage.py
import requests

# Disease risk scores
disease_risk_scores = { "Psoriasis": 3, "Malaria": 7, "Pneumonia": 8, "Dengue": 8 }

def get_icd10_code(disease):
    """ Fetches ICD-10 code for a disease using API """
    url = f"https://icd.who.int/api/{disease.replace(' ', '%20')}"
    response = requests.get(url)
    return response.json().get("icd10", "Unknown") if response.status_code == 200 else "Unknown"

def triage_category(disease, confidence):
    """ Determines the triage category based on risk and confidence """
    icd_code = get_icd10_code(disease)
    risk_score = disease_risk_scores.get(disease.title(), 3)
    if confidence < 0.10 and risk_score <= 3:
        return "🟢 Green (Home Care)"
    elif risk_score <= 3:
        return "🟢 Green (Home Care)"
    elif risk_score <= 6:
        return "🟡 Yellow (Doctor Visit)"
    else:
        return "🔴 Red (Emergency)"
