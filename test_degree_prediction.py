"""
Test Script for Degree Requirement Prediction

Run this with:
  PowerShell: cat test_degree_prediction.py | python manage.py shell
  CMD:        python manage.py shell < test_degree_prediction.py
  
Or in Django shell:
  python manage.py shell
  >>> exec(open('test_degree_prediction.py').read())
"""

print("=" * 60)
print("Testing Degree Requirement Prediction Integration")
print("=" * 60)

# Test 1: Import the predictor
print("\n[Test 1] Importing degree predictor...")
try:
    from ml_models.predictors.degree_predictor import degree_predictor
    print("✓ Successfully imported degree_predictor")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    exit(1)

# Test 2: Check model loaded
print("\n[Test 2] Checking model and features loaded...")
if degree_predictor.model is not None:
    print("✓ Model loaded successfully")
else:
    print("✗ Model not loaded")

if degree_predictor.features is not None:
    print(f"✓ Features loaded successfully ({len(degree_predictor.features)} features)")
    print(f"  Features: {degree_predictor.features}")
else:
    print("✗ Features not loaded")

# Test 3: Test prediction with valid data
print("\n[Test 3] Testing prediction with valid data...")
test_data_1 = {
    'skill_count': 5,
    'job_title_short': 'Software Engineer',
    'job_via': 'LinkedIn',
    'company_name': 'Google',
    'job_country': 'United States',
    'search_location': 'San Francisco'
}

try:
    result = degree_predictor.predict(test_data_1)
    if result.get('success'):
        print("✓ Prediction successful")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Degree Required: {result['degree_required']}")
        print(f"  Confidence: {result['confidence']}")
    else:
        print(f"✗ Prediction failed: {result.get('error')}")
except Exception as e:
    print(f"✗ Exception during prediction: {e}")

# Test 4: Test with different data
print("\n[Test 4] Testing with entry-level position...")
test_data_2 = {
    'skill_count': 2,
    'job_title_short': 'Sales Associate',
    'job_via': 'Indeed',
    'company_name': 'Retail Store',
    'job_country': 'United States',
    'search_location': 'New York'
}

try:
    result = degree_predictor.predict(test_data_2)
    if result.get('success'):
        print("✓ Prediction successful")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Degree Required: {result['degree_required']}")
        print(f"  Confidence: {result['confidence']}")
    else:
        print(f"✗ Prediction failed: {result.get('error')}")
except Exception as e:
    print(f"✗ Exception during prediction: {e}")

# Test 5: Test validation - missing fields
print("\n[Test 5] Testing input validation (missing fields)...")
invalid_data = {
    'skill_count': 3,
    'job_title_short': 'Developer'
    # Missing other required fields
}

result = degree_predictor.predict(invalid_data)
if not result.get('success'):
    print("✓ Validation working - caught missing fields")
    print(f"  Error: {result.get('error')}")
else:
    print("✗ Validation failed - should have rejected invalid input")

# Test 6: Test validation - invalid skill count
print("\n[Test 6] Testing input validation (invalid skill count)...")
invalid_data_2 = {
    'skill_count': 'not a number',
    'job_title_short': 'Developer',
    'job_via': 'LinkedIn',
    'company_name': 'Company',
    'job_country': 'USA',
    'search_location': 'City'
}

result = degree_predictor.predict(invalid_data_2)
if not result.get('success'):
    print("✓ Validation working - caught invalid skill count")
    print(f"  Error: {result.get('error')}")
else:
    print("✗ Validation failed - should have rejected invalid skill count")

# Test 7: Test the Django form
print("\n[Test 7] Testing Django form...")
try:
    from predictions.forms import DegreePredictionForm
    
    # Valid form data
    form_data = {
        'skill_count': 4,
        'job_title_short': 'Data Analyst',
        'job_via': 'LinkedIn',
        'company_name': 'Microsoft',
        'job_country': 'Canada',
        'search_location': 'Toronto'
    }
    
    form = DegreePredictionForm(data=form_data)
    if form.is_valid():
        print("✓ Django form validation passed")
        print(f"  Cleaned data: {form.cleaned_data}")
    else:
        print(f"✗ Django form validation failed: {form.errors}")
except Exception as e:
    print(f"✗ Exception testing form: {e}")

# Summary
print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)
print("All basic tests completed!")
print("\nNext steps:")
print("1. Run the development server: python manage.py runserver")
print("2. Navigate to: http://localhost:8000/predictions/job-seekers/")
print("3. Click 'Recommend Degree' and test the full integration")
print("=" * 60)
