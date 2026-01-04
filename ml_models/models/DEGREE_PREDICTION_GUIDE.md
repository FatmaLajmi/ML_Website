# Degree Requirement Prediction - Integration Guide

## Overview
This document describes the integration of the XGBoost degree requirement prediction model into the Django ML_BI_WEBSITE platform.

## Model Details

### Files
- **Model File**: `xgb_classifier_model(jojo).pkl`
- **Features File**: `xgb_features(jojo).pkl`
- **Location**: `ml_models/models/`

### Model Features
The XGBoost classifier uses 6 features to predict whether a job posting requires a degree:

1. **skill_count** (int): Number of skills mentioned in the job posting
2. **job_title_short** (str): Simplified/standardized job title
3. **job_via** (str): Platform where the job was posted (e.g., LinkedIn, Indeed)
4. **company_name** (str): Name of the hiring company
5. **job_country** (str): Country where the job is located
6. **search_location** (str): Specific city or location for the job

### Output
- **Binary Classification**: 
  - `1` = Degree Required
  - `0` = No Degree Required
- **Confidence Score**: Probability-based confidence percentage (if available)

## Implementation Components

### 1. Predictor Module
**File**: `ml_models/predictors/degree_predictor.py`

The `DegreePredictor` class handles:
- Model loading from pickle files
- Input validation
- Feature preparation
- Prediction execution
- Result formatting

**Usage Example**:
```python
from ml_models.predictors.degree_predictor import degree_predictor

input_data = {
    'skill_count': 5,
    'job_title_short': 'Software Engineer',
    'job_via': 'LinkedIn',
    'company_name': 'Google',
    'job_country': 'United States',
    'search_location': 'San Francisco'
}

result = degree_predictor.predict(input_data)
# Returns: {
#     'success': True,
#     'prediction': 'Degree Required',
#     'degree_required': True,
#     'confidence': '87.5%'
# }
```

### 2. Django Form
**File**: `predictions/forms.py`

The `DegreePredictionForm` class provides:
- HTML form fields for all 6 features
- Client-side validation
- Bootstrap styling
- Help text for user guidance

### 3. Django View
**File**: `predictions/views.py`

The `job_seeker_predictions_view` function:
- Handles GET requests to display the form
- Processes POST requests with form data
- Calls the predictor
- Returns results to the template
- Manages success/error messages

### 4. Template
**File**: `predictions/templates/predictions/jobSeekersPredictions.html`

Features:
- Bootstrap modal for the prediction form
- Form fields with validation errors
- Result display with visual indicators
- Auto-open modal on form submission
- Success/error message display

## How to Use

### For End Users

1. **Access the Page**: Navigate to `/predictions/job-seekers/`
2. **Open Modal**: Click "Recommend Degree" button
3. **Fill Form**: Enter the 6 required fields:
   - Skill Count (number)
   - Job Title Short (text)
   - Job Via (text)
   - Company Name (text)
   - Job Country (text)
   - Search Location (text)
4. **Submit**: Click "Predict Degree Requirement"
5. **View Result**: See the prediction and confidence score

### For Developers

#### Testing the Predictor
```python
# In Django shell: python manage.py shell
from ml_models.predictors.degree_predictor import degree_predictor

# Test prediction
test_data = {
    'skill_count': 3,
    'job_title_short': 'Data Analyst',
    'job_via': 'Indeed',
    'company_name': 'Microsoft',
    'job_country': 'Canada',
    'search_location': 'Toronto'
}

result = degree_predictor.predict(test_data)
print(result)
```

#### Adding New Features
To extend the model with additional features:
1. Retrain the model with new features
2. Update `xgb_features(jojo).pkl` with new feature list
3. Update `DegreePredictionForm` in `forms.py`
4. Update `_prepare_features()` in `degree_predictor.py`
5. Update the template form fields

## Error Handling

The predictor handles various error scenarios:

1. **Missing Model Files**: Returns error message if .pkl files not found
2. **Invalid Input**: Validates all required fields
3. **Prediction Errors**: Catches and reports prediction failures
4. **Type Errors**: Validates skill_count is numeric

## Dependencies

Required Python packages (in `requirements.txt`):
- `pandas>=2.0.0`
- `xgboost>=2.0.0`
- `scikit-learn>=1.3.0`
- `numpy>=1.24.0`

## Deployment Checklist

- [x] Model files placed in `ml_models/models/`
- [x] Predictor module created with proper imports
- [x] Django form defined with all fields
- [x] View handles POST requests correctly
- [x] Template includes form and result display
- [x] XGBoost added to requirements.txt
- [x] Error handling implemented
- [x] Messages framework integrated
- [ ] Run migrations if needed: `python manage.py migrate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test prediction functionality
- [ ] Verify model loads on server startup

## Testing

### Manual Testing Steps
1. Start the development server: `python manage.py runserver`
2. Navigate to `/predictions/job-seekers/`
3. Click "Recommend Degree"
4. Fill out the form with test data
5. Submit and verify prediction appears
6. Test with various inputs to check edge cases

### Example Test Cases

**Case 1: Senior Tech Role**
- skill_count: 8
- job_title_short: Senior Software Engineer
- job_via: LinkedIn
- company_name: Google
- job_country: United States
- search_location: Mountain View
- Expected: Degree Required

**Case 2: Entry Level Role**
- skill_count: 2
- job_title_short: Sales Associate
- job_via: Indeed
- company_name: Local Store
- job_country: United States
- search_location: Small Town
- Expected: No Degree Required

## Troubleshooting

### Model Not Loading
**Issue**: "Degree prediction model is not available"
**Solution**: 
- Check that .pkl files exist in `ml_models/models/`
- Verify file names match exactly
- Check file permissions
- Review server logs for loading errors

### Prediction Errors
**Issue**: Prediction fails with error message
**Solution**:
- Verify all form fields are filled
- Check data types (skill_count must be integer)
- Ensure pandas and xgboost are installed
- Check model compatibility with xgboost version

### Form Not Displaying
**Issue**: Modal doesn't open or form is missing
**Solution**:
- Verify URL is correctly configured in `urls.py`
- Check that view is passing `degree_form` to context
- Ensure template extends correct base template
- Verify Bootstrap JS/CSS are loaded

## Performance Considerations

- Model is loaded once at startup (singleton pattern)
- Predictions are fast (<100ms typically)
- No database queries required for prediction
- Suitable for real-time user interactions

## Future Enhancements

Potential improvements:
1. Add feature importance visualization
2. Implement batch prediction for multiple jobs
3. Add prediction history logging
4. Create API endpoint for external access
5. Add A/B testing framework
6. Implement model versioning
7. Add prediction explanations (SHAP values)
8. Cache frequent predictions

## Support

For issues or questions:
- Check Django logs for detailed error messages
- Review model loading output in console
- Test predictor directly in Django shell
- Verify all dependencies are installed

---
Last Updated: January 3, 2026
