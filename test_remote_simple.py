"""
Test direct du modèle remote_work sans Django
"""
import joblib
import pandas as pd
from pathlib import Path

print("=" * 70)
print("TEST DIRECT DU MODÈLE REMOTE WORK")
print("=" * 70)

# Charger le modèle directement
model_path = Path("ml_models/models/remote_work_v3(eya).pkl")
print(f"\nChargement du modèle depuis: {model_path}")
print(f"Modèle existe: {model_path.exists()}")

if model_path.exists():
    model = joblib.load(model_path)
    print(f"✓ Modèle chargé avec succès")
    print(f"  Type: {type(model)}")
    
    # Test 1: Données CLAIREMENT remote
    print("\n" + "-" * 70)
    print("TEST 1: Données CLAIREMENT REMOTE")
    print("-" * 70)
    
    X1 = pd.DataFrame([{
        "job_title_short": "Remote Software Engineer",
        "job_seniority": "Senior",
        "job_country": "US",
        "job_schedule_type": "Fully Remote",
        "job_via": "Unknown",
        "posted_month": 1,
        "posted_quarter": 1,
        "text_block": "Remote work fully remote work from home anywhere world flexible work from anywhere remote position work remotely"
    }])
    
    print(f"Input:\n{X1.to_dict('records')[0]}\n")
    
    try:
        pred1 = model.predict(X1)[0]
        proba1 = model.predict_proba(X1)[0]
        
        print(f"Prediction: {pred1}")
        print(f"Probabilities: {proba1}")
        print(f"Remote prob (index 1): {proba1[1] * 100:.2f}%")
        print(f"Résultat: {'Remote' if proba1[1] >= 0.5 else 'On-site'}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 2: Données ON-SITE
    print("\n" + "-" * 70)
    print("TEST 2: Données ON-SITE")
    print("-" * 70)
    
    X2 = pd.DataFrame([{
        "job_title_short": "Office Manager",
        "job_seniority": "Junior",
        "job_country": "FR",
        "job_schedule_type": "On-site",
        "job_via": "Unknown",
        "posted_month": 1,
        "posted_quarter": 1,
        "text_block": "Office based on-site office location Paris headquarters in-office"
    }])
    
    print(f"Input:\n{X2.to_dict('records')[0]}\n")
    
    try:
        pred2 = model.predict(X2)[0]
        proba2 = model.predict_proba(X2)[0]
        
        print(f"Prediction: {pred2}")
        print(f"Probabilities: {proba2}")
        print(f"Remote prob (index 1): {proba2[1] * 100:.2f}%")
        print(f"Résultat: {'Remote' if proba2[1] >= 0.5 else 'On-site'}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    # Test 3: Données HYBRIDE
    print("\n" + "-" * 70)
    print("TEST 3: Données HYBRIDE")
    print("-" * 70)
    
    X3 = pd.DataFrame([{
        "job_title_short": "Data Analyst",
        "job_seniority": "Mid",
        "job_country": "UK",
        "job_schedule_type": "Hybrid",
        "job_via": "Unknown",
        "posted_month": 1,
        "posted_quarter": 1,
        "text_block": "Hybrid work 3 days office 2 days remote flexible arrangement"
    }])
    
    print(f"Input:\n{X3.to_dict('records')[0]}\n")
    
    try:
        pred3 = model.predict(X3)[0]
        proba3 = model.predict_proba(X3)[0]
        
        print(f"Prediction: {pred3}")
        print(f"Probabilities: {proba3}")
        print(f"Remote prob (index 1): {proba3[1] * 100:.2f}%")
        print(f"Résultat: {'Remote' if proba3[1] >= 0.5 else 'On-site'}")
    except Exception as e:
        print(f"ERREUR: {e}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("✓ Si Test 1 montre Remote > 50%, le modèle fonctionne correctement")
    print("✗ Si tous les tests montrent On-site, le modèle est trop biaisé")
    
else:
    print(f"✗ ERREUR: Le modèle n'existe pas à {model_path}")
