"""
Test DIRECT avec les bonnes valeurs du modèle
Aucun texte 'remote', juste les métadonnées
"""
import joblib
import pandas as pd
from pathlib import Path

model_path = Path("ml_models/models/remote_work_v3(eya).pkl")
model = joblib.load(model_path)

print("=" * 70)
print("TEST AVEC VALEURS EXACTES DU MODÈLE")
print("=" * 70)

# Test 1: Data Scientist Senior - probablement remote
print("\nTEST 1: Data Scientist - Senior")
print("-" * 70)

X1 = pd.DataFrame([{
    "job_title_short": "Data Scientist",
    "job_seniority": "Senior",
    "job_country": "United States",
    "job_schedule_type": "Full-time",
    "job_via": "Unknown",
    "posted_month": 1,
    "posted_quarter": 1,
    "text_block": "Looking for talented data scientist to join our team"
}])

pred1 = model.predict(X1)[0]
proba1 = model.predict_proba(X1)[0]
print(f"Prediction: {pred1}")
print(f"Probabilities: [on-site: {proba1[0]*100:.2f}%, remote: {proba1[1]*100:.2f}%]")
print(f"Résultat: {'✓ REMOTE' if proba1[1] >= 0.5 else '✗ ON-SITE'}")

# Test 2: Business Analyst Lead - probablement on-site
print("\nTEST 2: Business Analyst - Lead")
print("-" * 70)

X2 = pd.DataFrame([{
    "job_title_short": "Business Analyst",
    "job_seniority": "Lead",
    "job_country": "United Kingdom",
    "job_schedule_type": "Full-time",
    "job_via": "Unknown",
    "posted_month": 1,
    "posted_quarter": 1,
    "text_block": "Business analyst position in London office"
}])

pred2 = model.predict(X2)[0]
proba2 = model.predict_proba(X2)[0]
print(f"Prediction: {pred2}")
print(f"Probabilities: [on-site: {proba2[0]*100:.2f}%, remote: {proba2[1]*100:.2f}%]")
print(f"Résultat: {'✓ REMOTE' if proba2[1] >= 0.5 else '✗ ON-SITE'}")

# Test 3: Cloud Engineer Mid
print("\nTEST 3: Cloud Engineer - Mid")
print("-" * 70)

X3 = pd.DataFrame([{
    "job_title_short": "Cloud Engineer",
    "job_seniority": "Mid",
    "job_country": "Canada",
    "job_schedule_type": "Full-time",
    "job_via": "Unknown",
    "posted_month": 1,
    "posted_quarter": 1,
    "text_block": "Cloud engineer position"
}])

pred3 = model.predict(X3)[0]
proba3 = model.predict_proba(X3)[0]
print(f"Prediction: {pred3}")
print(f"Probabilities: [on-site: {proba3[0]*100:.2f}%, remote: {proba3[1]*100:.2f}%]")
print(f"Résultat: {'✓ REMOTE' if proba3[1] >= 0.5 else '✗ ON-SITE'}")

print("\n" + "=" * 70)
print("RÉSUMÉ")
print("=" * 70)

if proba1[1] > 0.5:
    print(f"✓ Le modèle PEUT prédire Remote!")
    print(f"  Data Scientist Senior: {proba1[1]*100:.2f}% remote")
else:
    print(f"✗ Le modèle est toujours biaisé On-site")
    print(f"  Même Data Scientist Senior: seulement {proba1[1]*100:.2f}% remote")
