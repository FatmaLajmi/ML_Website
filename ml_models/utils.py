"""
Utility functions shared across ML models
Helper functions for common operations
"""
import json
from datetime import datetime


def format_prediction_result(prediction, model_type, confidence=None):
    """
    Format prediction results for display
    Args:
        prediction: Raw prediction from model
        model_type: Type of prediction (salary, job_title, etc.)
        confidence: Optional confidence score
    Returns:
        Formatted result dictionary
    """
    result = {
        'prediction': prediction,
        'model_type': model_type,
        'timestamp': datetime.now().isoformat(),
    }
    
    if confidence is not None:
        result['confidence'] = confidence
    
    return result


def log_prediction(user_id, model_type, input_data, prediction):
    """
    Log prediction for analytics and monitoring
    Args:
        user_id: ID of the user making the prediction
        model_type: Type of prediction
        input_data: Input data used
        prediction: Prediction result
    """
    log_entry = {
        'user_id': user_id,
        'model_type': model_type,
        'input_data': input_data,
        'prediction': prediction,
        'timestamp': datetime.now().isoformat(),
    }
    
    # In production, this would write to a proper logging system
    print(f"Prediction logged: {json.dumps(log_entry)}")
    
    return log_entry


def calculate_confidence_interval(prediction, std_dev=None):
    """
    Calculate confidence interval for numerical predictions
    Args:
        prediction: Point prediction
        std_dev: Standard deviation if available
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    if std_dev is None:
        # Default to 10% margin if no std_dev provided
        margin = prediction * 0.1
    else:
        # 95% confidence interval (±1.96 std deviations)
        margin = 1.96 * std_dev
    
    return (prediction - margin, prediction + margin)


def normalize_job_title(title):
    """Normalize job title for consistency"""
    if not title:
        return ""
    
    # Common normalizations
    title = title.strip().title()
    
    # Replace common abbreviations
    replacements = {
        'Sr.': 'Senior',
        'Jr.': 'Junior',
        'Mgr': 'Manager',
        'Dev': 'Developer',
        'Eng': 'Engineer',
    }
    
    for abbr, full in replacements.items():
        title = title.replace(abbr, full)
    
    return title


def parse_salary_range(min_salary, max_salary):
    """Format salary range for display"""
    if min_salary and max_salary:
        return f"${min_salary:,.2f} - ${max_salary:,.2f}"
    elif min_salary:
        return f"${min_salary:,.2f}+"
    elif max_salary:
        return f"Up to ${max_salary:,.2f}"
    else:
        return "Not specified"


def get_experience_level(years):
    """Categorize experience years into levels"""
    if years < 2:
        return "Entry Level"
    elif years < 5:
        return "Mid Level"
    elif years < 10:
        return "Senior Level"
    else:
        return "Expert Level"
