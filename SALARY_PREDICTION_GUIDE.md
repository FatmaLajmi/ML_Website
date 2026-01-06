# Salary Prediction Feature - Complete Documentation

## Overview
The Salary Prediction feature uses a regression model to estimate salary based on job characteristics.
- **Model**: `salary_regression_model(zeineb+eya).pkl`
- **Type**: Regression (predicts log-salary, converted back to actual salary)
- **Access**: All authenticated users (Job Seekers and Employers)
- **URL**: `/predictions/salary/`

## Architecture

### 1. **Form** (`predictions/forms.py`)
Class: `SalaryPredictionForm`

**Input Fields:**
- `job_title_short` (Text): Job title (e.g., "Data Scientist")
- `job_country` (Dropdown): Country (US, CA, UK, etc.)
- `job_state` (Dropdown): State/Region (CA, NY, TX, etc.) - Optional
- `skills_text` (Textarea): Comma-separated skills

### 2. **Predictor** (`ml_models/predictors/salary_predictor_regression.py`)
Function: `predict_salary(data: dict) -> dict`

**Features Processed:**
```
Input Features (User-provided):
├── job_title_short (normalized, lowercased)
├── job_country (default: "US")
├── job_state (default: "Unknown")
├── skills_text (normalized, lowercased)
└── company_size (default: "Medium")

Calculated Features (Backend):
├── num_skills (count from comma-separated skills)
├── short_title_length (character length of job title)
└── title_length (same as short_title_length)
```

**Processing Flow:**
1. Validate input fields
2. Load the regression model
3. Normalize and clean inputs
4. Calculate numerical features
5. Create DataFrame with all features
6. Make prediction (predicts log-salary)
7. Convert log-salary to actual salary using `exp()`
8. Return result with formatted salary

### 3. **View** (`predictions/views.py`)
Function: `salary_prediction_page(request)`

**Features:**
- Login required (`@login_required`)
- Handles GET (displays form) and POST (processes prediction)
- Shows success/error messages
- Renders result on the same page

### 4. **Template** (`predictions/templates/predictions/salary.html`)
Beautiful, responsive template with:
- Form section (left column)
- Results section (right column)
- Gradient styling with purple/pink theme
- Information cards explaining how it works
- Success/error alerts

### 5. **URL Routing** (`predictions/urls.py`)
```python
path("salary/", views.salary_prediction_page, name="salary")
```

### 6. **Navigation** (`jobTemplate/jobx-free-lite/base.html`)
- Added to Job Seeker dropdown menu
- Added to Employer dropdown menu
- Icon: `lni-money-location`

## Model Details

### Model Type: XGBoost / Sklearn Regression
- **Target Variable**: `log_salary_year`
- **Input Features**: 8 features (4 categorical + 4 numerical)
- **Output**: Log-transformed salary (converted back using `np.exp()`)

### Feature Specifications
| Feature | Type | Example |
|---------|------|---------|
| job_title_short | Categorical | "data scientist" |
| job_country | Categorical | "us" |
| job_state | Categorical | "ca" |
| company_size | Categorical | "medium" |
| skills_text | Text | "python, sql, ml" |
| num_skills | Numerical | 3 |
| title_length | Numerical | 16 |
| short_title_length | Numerical | 16 |

## Usage Example

### Python Script
```python
from ml_models.predictors.salary_predictor_regression import predict_salary

data = {
    'job_title_short': 'Data Scientist',
    'job_country': 'US',
    'job_state': 'CA',
    'skills_text': 'python, sql, machine learning, aws',
}

result = predict_salary(data)
print(result)
# Output:
# {
#     'success': True,
#     'prediction': '$125,000',
#     'salary_value': 125000.0,
#     'job_title': 'data scientist',
#     'num_skills': 4,
#     'log_salary': 11.7321
# }
```

### Django View
```python
# Automatically called by salary_prediction_page view
form = SalaryPredictionForm(request.POST)
if form.is_valid():
    result = predict_salary(form.cleaned_data)
```

## Error Handling

The function returns a `success` field to indicate whether prediction worked:

```python
# Success
{
    'success': True,
    'prediction': '$92,500',
    ...
}

# Failure
{
    'success': False,
    'error': 'Job title is required'
}
```

**Validation Errors:**
- Missing job title
- Missing country
- Missing skills
- Model file not found
- Feature preparation errors

## Testing

Run the test script:
```bash
python test_salary_prediction.py
```

This tests 3 different job profiles:
1. Data Scientist (6 skills)
2. Software Engineer (5 skills)
3. Product Manager (4 skills)

## Integration Checklist

- [x] Form created with proper fields
- [x] Predictor function with feature engineering
- [x] View function with error handling
- [x] Beautiful template with styling
- [x] URL routing configured
- [x] Navigation links added (Job Seeker + Employer)
- [x] Model loader updated to load PKL file
- [x] Test script created

## File Structure
```
predictions/
├── forms.py                 # SalaryPredictionForm
├── views.py                # salary_prediction_page()
├── urls.py                 # URL routing
├── templates/
│   └── predictions/
│       └── salary.html     # Beautiful template

ml_models/
├── predictors/
│   └── salary_predictor_regression.py  # predict_salary()
└── models/
    └── salary_regression_model(zeineb+eya).pkl

jobTemplate/jobx-free-lite/
└── base.html               # Navigation links

Root:
└── test_salary_prediction.py  # Test script
```

## Next Steps (Optional Enhancements)
1. Add experience level input
2. Add education level input
3. Add bonus/benefits estimation
4. Add salary trend analysis over time
5. Add company comparison feature
6. Add export to PDF functionality

## Troubleshooting

### "Model file not found" error
- Ensure `salary_regression_model(zeineb+eya).pkl` exists in `ml_models/models/`
- Check the exact filename in the error message

### "ValueError: feature mismatch"
- Model expects specific column names
- Check that all 8 features are in the DataFrame
- Ensure categorical values are properly normalized

### Form validation errors
- All 3 main fields (job_title, country, skills) are required
- Job state is optional

## Authors
- Zeineb
- Eya

**Date**: January 2026
