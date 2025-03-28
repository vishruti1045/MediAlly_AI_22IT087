import joblib
from sklearn.preprocessing import LabelEncoder

# ✅ Define your list of diseases
diseases = [
    "Psoriasis", "Varicose Veins", "Typhoid", "Chicken pox", "Impetigo", "Dengue",
    "Fungal infection", "Common Cold", "Pneumonia", "Dimorphic Hemorrhoids", "Arthritis",
    "Acne", "Bronchial Asthma", "Hypertension", "Migraine", "Cervical spondylosis",
    "Jaundice", "Malaria", "urinary tract infection", "allergy",
    "gastroesophageal reflux disease", "drug reaction", "peptic ulcer disease", "diabetes"
]

# ✅ Initialize and fit Label Encoder
label_encoder = LabelEncoder()
label_encoder.fit(diseases)

# ✅ Save Label Encoder Properly
joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ label_encoder.pkl has been successfully saved!")
