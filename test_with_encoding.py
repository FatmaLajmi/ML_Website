"""
Test avec la fonction mise à jour
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml_models.predictors.remote_work_predictor import predict_remote_work

print("=" * 70)
print("TEST AVEC ENCODING DES FEATURES")
print("=" * 70)

# Test 1: Données CLAIREMENT remote
print("\nTEST 1: Données CLAIREMENT REMOTE")
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
print("\nTEST 2: Données ON-SITE")
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
print("\nTEST 3: Données HYBRIDE")
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

print("\n" + "=" * 70)
print("ANALYSE")
print("=" * 70)

if result_1.get('success'):
    proba_1 = result_1.get('proba_remote_pct', 0)
    proba_2 = result_2.get('proba_remote_pct', 0) if result_2.get('success') else 0
    proba_3 = result_3.get('proba_remote_pct', 0) if result_3.get('success') else 0
    
    print(f"\nProbabilités Remote:")
    print(f"  Test 1 (Clairement Remote): {proba_1}%")
    print(f"  Test 2 (On-site): {proba_2}%")
    print(f"  Test 3 (Hybride): {proba_3}%")
    
    if proba_1 > 50 and proba_2 < 50:
        print(f"\n✓ SUCCÈS! Le modèle fonctionne correctement!")
    else:
        print(f"\n✗ PROBLÈME: Les résultats ne sont pas cohérents")
else:
    print(f"Erreur: {result_1.get('error')}")
