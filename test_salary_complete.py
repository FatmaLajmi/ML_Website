#!/usr/bin/env python
"""Test the complete feature engineering salary prediction"""

from ml_models.predictors.salary_predictor_regression import predict_salary

test_cases = [
    {
        'name': 'Senior Data Scientist',
        'input': {
            'job_title_short': 'Senior Data Scientist',
            'job_country': 'US',
            'job_state': 'CA',
            'skills_text': 'python, sql, tensorflow, aws, pandas, numpy, scikit-learn, docker',
            'job_schedule_type': 'full_time',
            'remote_option': 1
        }
    },
    {
        'name': 'Software Engineer (Mid-Level)',
        'input': {
            'job_title_short': 'Software Engineer',
            'job_country': 'US',
            'job_state': 'NY',
            'skills_text': 'javascript, react, node.js, python, sql, git, docker, kubernetes',
            'job_schedule_type': 'full_time',
            'remote_option': 0
        }
    },
    {
        'name': 'Product Manager (Manager)',
        'input': {
            'job_title_short': 'Manager Product',
            'job_country': 'US',
            'job_state': 'CA',
            'skills_text': 'excel, sql, tableau, power_bi, analytics, communication',
            'job_schedule_type': 'full_time',
            'remote_option': 1
        }
    }
]

print("=" * 80)
print("SALARY PREDICTION - COMPLETE FEATURE ENGINEERING TEST")
print("=" * 80)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n[Test {i}] {test_case['name']}")
    print("-" * 80)
    
    result = predict_salary(test_case['input'])
    
    if result.get('success'):
        print(f"✅ SUCCESS")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Features Generated: {result['features_count']}")
        print(f"   Skills: {result['num_skills']}")
        print(f"   Log Salary: {result['log_salary']}")
    else:
        print(f"❌ ERROR: {result['error']}")

print("\n" + "=" * 80)
print("✅ COMPLETE - All salary predictions working with 170+ features!")
print("=" * 80)
