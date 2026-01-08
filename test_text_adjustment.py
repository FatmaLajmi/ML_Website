"""
Test avec l'ajustement du texte
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ml_models.predictors.remote_work_predictor import predict_remote_work

print("=" * 70)
print("TEST AVEC AJUSTEMENT TEXTUEL")
print("=" * 70)

# Test 1: Data Scientist avec "remote" dans la description
print("\nTEST 1: Data Scientist - Avec keyword 'remote'")
print("-" * 70)

test_data_1 = {
    "job_title_short": "Data Scientist",
    "job_seniority": "Senior",
    "job_country": "United States",
    "job_schedule_type": "Full-time",
    "text_block": "We are looking for a senior data scientist for a fully remote position. Work from anywhere in the world. Flexible schedule. Remote work from home."
}

result_1 = predict_remote_work(test_data_1)
print(f"Résultat: {result_1}")

# Test 2: Data Scientist SANS "remote"
print("\nTEST 2: Data Scientist - SANS keyword 'remote'")
print("-" * 70)

test_data_2 = {
    "job_title_short": "Data Scientist",
    "job_seniority": "Senior",
    "job_country": "United States",
    "job_schedule_type": "Full-time",
    "text_block": "Join our team as a senior data scientist. Analyze data and build models."
}

result_2 = predict_remote_work(test_data_2)
print(f"Résultat: {result_2}")

# Test 3: Cloud Engineer avec "work from home"
print("\nTEST 3: Cloud Engineer - Avec keyword 'work from home'")
print("-" * 70)

test_data_3 = {
    "job_title_short": "Cloud Engineer",
    "job_seniority": "Mid",
    "job_country": "Canada",
    "job_schedule_type": "Full-time",
    "text_block": "Work from home opportunity! This is a WFH position with flexible hours. Remote team."
}

result_3 = predict_remote_work(test_data_3)
print(f"Résultat: {result_3}")

# Test 4: Business Analyst avec "on-site"
print("\nTEST 4: Business Analyst - Avec keyword 'on-site'")
print("-" * 70)

test_data_4 = {
    "job_title_short": "Business Analyst",
    "job_seniority": "Lead",
    "job_country": "United Kingdom",
    "job_schedule_type": "Full-time",
    "text_block": "Must be on-site in our London office. In-person collaboration required. Reporting to office daily."
}

result_4 = predict_remote_work(test_data_4)
print(f"Résultat: {result_4}")

print("\n" + "=" * 70)
print("RÉSUMÉ")
print("=" * 70)

if result_1.get('success'):
    proba_1 = result_1.get('proba_remote_pct', 0)
    proba_2 = result_2.get('proba_remote_pct', 0)
    proba_3 = result_3.get('proba_remote_pct', 0)
    proba_4 = result_4.get('proba_remote_pct', 0)
    
    print(f"\nTest 1 (avec 'remote'): {proba_1}% → {result_1['prediction']}")
    print(f"Test 2 (sans 'remote'): {proba_2}% → {result_2['prediction']}")
    print(f"Test 3 (avec 'work from home'): {proba_3}% → {result_3['prediction']}")
    print(f"Test 4 (avec 'on-site'): {proba_4}% → {result_4['prediction']}")
    
    if result_1['prediction'] == 'Remote':
        print(f"\n✓ SUCCÈS! Maintenant vous pouvez voir 'Remote' dans les résultats!")
    else:
        print(f"\n✗ Les résultats ne changent pas encore")
