"""
Script de test du modèle remote_work_predictor
pour diagnostiquer pourquoi il prédit toujours on-site
"""
import os
import django
import sys
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WEBSITE.settings')
django.setup()

from ml_models.predictors.remote_work_predictor import predict_remote_work
import joblib

print("=" * 70)
print("TEST DU MODÈLE REMOTE WORK")
print("=" * 70)

# Charger le modèle directement
model_path = Path(__file__).parent / "ml_models" / "models" / "remote_work_v3(eya).pkl"
print(f"\nChargement du modèle depuis: {model_path}")
print(f"Modèle existe: {model_path.exists()}")

if model_path.exists():
    model = joblib.load(model_path)
    print(f"✓ Modèle chargé avec succès")
    print(f"  Type: {type(model)}")
    
    # Vérifier les classes
    if hasattr(model, 'classes_'):
        print(f"  Classes: {model.classes_}")
    
    # Test 1: Données CLAIREMENT remote
    print("\n" + "-" * 70)
    print("TEST 1: Données CLAIREMENT REMOTE")
    print("-" * 70)
    
    test_data_1 = {
        "job_title_short": "Remote Software Engineer",
        "job_seniority": "Senior",
        "job_country": "US",
        "job_schedule_type": "Fully Remote",
        "text_block": "Remote work fully remote work from home anywhere world flexible work from anywhere remote position work remotely"
    }
    
    result_1 = predict_remote_work(test_data_1)
    print(f"Résultat: {result_1}")
    
    # Test 2: Données ON-SITE
    print("\n" + "-" * 70)
    print("TEST 2: Données ON-SITE")
    print("-" * 70)
    
    test_data_2 = {
        "job_title_short": "Office Manager",
        "job_seniority": "Junior",
        "job_country": "FR",
        "job_schedule_type": "On-site",
        "text_block": "Office based on-site office location Paris headquarters in-office"
    }
    
    result_2 = predict_remote_work(test_data_2)
    print(f"Résultat: {result_2}")
    
    # Test 3: Données HYBRIDE
    print("\n" + "-" * 70)
    print("TEST 3: Données HYBRIDE")
    print("-" * 70)
    
    test_data_3 = {
        "job_title_short": "Data Analyst",
        "job_seniority": "Mid",
        "job_country": "UK",
        "job_schedule_type": "Hybrid",
        "text_block": "Hybrid work 3 days office 2 days remote flexible arrangement"
    }
    
    result_3 = predict_remote_work(test_data_3)
    print(f"Résultat: {result_3}")
    
    # Test 4: Données vides/minimalistes
    print("\n" + "-" * 70)
    print("TEST 4: Données MINIMALISTES")
    print("-" * 70)
    
    test_data_4 = {
        "job_title_short": "Engineer",
        "job_seniority": "Mid",
        "job_country": "US",
        "job_schedule_type": "Full-time",
        "text_block": "Position available"
    }
    
    result_4 = predict_remote_work(test_data_4)
    print(f"Résultat: {result_4}")
    
    print("\n" + "=" * 70)
    print("ANALYSE")
    print("=" * 70)
    
    proba_1 = result_1.get('proba_remote_pct', 0) if result_1.get('success') else 0
    proba_2 = result_2.get('proba_remote_pct', 0) if result_2.get('success') else 0
    proba_3 = result_3.get('proba_remote_pct', 0) if result_3.get('success') else 0
    proba_4 = result_4.get('proba_remote_pct', 0) if result_4.get('success') else 0
    
    print(f"\nProbabilités Remote:")
    print(f"  Test 1 (Clairement Remote): {proba_1}%")
    print(f"  Test 2 (On-site): {proba_2}%")
    print(f"  Test 3 (Hybride): {proba_3}%")
    print(f"  Test 4 (Minimaliste): {proba_4}%")
    
    if proba_1 > 50:
        print(f"\n✓ Le modèle PEUT prédire Remote! (Test 1 = {proba_1}%)")
    else:
        print(f"\n✗ PROBLÈME: Le modèle prédit On-site même pour données clairement remote!")
        print(f"   Probabilité Test 1 = {proba_1}% (< 50%)")
        print(f"\n   Possibles causes:")
        print(f"   1. Le modèle est extrêmement biaisé vers on-site")
        print(f"   2. Les features ne correspondent pas aux données d'entraînement")
        print(f"   3. Les valeurs par défaut (job_via, posted_month) sont mauvaises")
        print(f"   4. Le modèle n'a pas été bien entraîné")

else:
    print(f"✗ ERREUR: Le modèle n'existe pas à {model_path}")

print("\n" + "=" * 70)
