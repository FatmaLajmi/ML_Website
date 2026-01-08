"""
Quick test script for Salary Prediction functionality
Tests the predict_salary function without Django
"""
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ml_models.predictors.salary_predictor_regression import predict_salary

# Test data
test_data_1 = {
    'job_title_short': 'Data Scientist',
    'job_country': 'US',
    'job_state': 'CA',
    'skills_text': 'python, sql, machine learning, tensorflow, aws, pandas',
    'company_size': 'Large',
}

test_data_2 = {
    'job_title_short': 'Software Engineer',
    'job_country': 'US',
    'job_state': 'NY',
    'skills_text': 'java, spring boot, microservices, docker, kubernetes',
}

test_data_3 = {
    'job_title_short': 'Product Manager',
    'job_country': 'US',
    'job_state': 'TX',
    'skills_text': 'product strategy, analytics, roadmap, stakeholder management',
}

print("=" * 60)
print("SALARY PREDICTION TEST")
print("=" * 60)

for i, test_data in enumerate([test_data_1, test_data_2, test_data_3], 1):
    print(f"\n📊 Test {i}: {test_data['job_title_short']}")
    print("-" * 60)
    result = predict_salary(test_data)
    
    if result.get('success'):
        print(f"✅ Success!")
        print(f"   Position: {result['job_title'].title()}")
        print(f"   Predicted Salary: {result['prediction']}")
        print(f"   Number of Skills: {result['num_skills']}")
        print(f"   Log-Salary: {result['log_salary']}")
    else:
        print(f"❌ Error: {result.get('error')}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
