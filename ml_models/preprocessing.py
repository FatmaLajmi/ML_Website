"""
Preprocessing utilities for ML model inputs
Feature encoding and transformations
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


class DataPreprocessor:
    """Handle data preprocessing for ML models"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scalers = {}
    
    def encode_categorical(self, data, column_name):
        """
        Encode categorical variables
        Args:
            data: Input data (string or list of strings)
            column_name: Name of the column being encoded
        Returns:
            Encoded data
        """
        if column_name not in self.label_encoders:
            self.label_encoders[column_name] = LabelEncoder()
        
        if isinstance(data, str):
            data = [data]
        
        # Check if encoder is fitted
        if hasattr(self.label_encoders[column_name], 'classes_'):
            return self.label_encoders[column_name].transform(data)
        else:
            return self.label_encoders[column_name].fit_transform(data)
    
    def scale_numerical(self, data, column_name):
        """
        Scale numerical features
        Args:
            data: Input data (number or array)
            column_name: Name of the column being scaled
        Returns:
            Scaled data
        """
        if column_name not in self.scalers:
            self.scalers[column_name] = StandardScaler()
        
        if isinstance(data, (int, float)):
            data = [[data]]
        elif isinstance(data, list):
            data = [[x] for x in data]
        
        # Check if scaler is fitted
        if hasattr(self.scalers[column_name], 'mean_'):
            return self.scalers[column_name].transform(data)
        else:
            return self.scalers[column_name].fit_transform(data)
    
    def prepare_feature_dict(self, input_data):
        """
        Convert input dictionary to format suitable for model prediction
        Args:
            input_data: Dictionary of feature names and values
        Returns:
            Processed feature array or DataFrame
        """
        # This will be customized based on specific model requirements
        df = pd.DataFrame([input_data])
        return df
    
    def clean_text_input(self, text):
        """Clean and normalize text input"""
        if not text:
            return ""
        return text.strip().lower()
    
    def parse_skills(self, skills_string):
        """Parse comma-separated skills string into list"""
        if not skills_string:
            return []
        return [skill.strip() for skill in skills_string.split(',') if skill.strip()]


# Global preprocessor instance
preprocessor = DataPreprocessor()

REQUIRED_COLUMNS = [
    "job_title_clean",
    "company_norm",
    "job_schedule_type_clean",
    "IsRemoteNum",
    "job_country",
    "company_target_smoothed",
    "company_freq",
    "job_country_grouped",
    "company_size",
]

def _clean_text(v):
    return (v or "").strip().lower()


def _normalize_schedule_type_for_model(v: str) -> str:
    """Map form values to the exact labels seen during model training."""
    s = _clean_text(v)
    if s in {"full-time", "full time", "fulltime"}:
        return "Full-Time"
    if s in {"part-time", "part time", "parttime"}:
        return "Part-Time"
    if s in {"contract", "contractor", "freelance"}:
        return "Contractor"
    if s in {"internship", "intern"}:
        return "Internship"
    if not s:
        return "Other"
    return "Other"


def _normalize_country_for_model(v: str) -> str:
    """Map form values to the exact country labels seen during model training."""
    c = (v or "").strip()
    if not c:
        return "Other"

    cl = c.strip().lower()
    if cl in {"usa", "us", "u.s.", "united states", "united states of america"}:
        return "United States"
    if cl in {"uk", "u.k.", "united kingdom", "great britain", "britain", "england", "scotland", "wales"}:
        return "United Kingdom"
    if cl == "other":
        return "Other"

    # For values like "Canada", "France", "Germany" coming from the ChoiceField.
    return c

def _country_group(country: str) -> str:
    c = _clean_text(country)
    if c in {"usa", "united states", "united states of america", "canada", "mexico"}:
        return "north_america"
    if c in {"uk", "united kingdom", "england", "scotland", "wales", "ireland",
             "france", "germany", "spain", "italy", "netherlands", "belgium", "sweden",
             "norway", "denmark", "finland", "switzerland", "austria", "portugal"}:
        return "europe"
    if c in {"india", "china", "japan", "south korea", "singapore", "vietnam", "philippines"}:
        return "asia"
    if not c:
        return "unknown"
    return "other"

def prepare_health_insurance_features(cleaned_data: dict) -> pd.DataFrame:
    raw_country = cleaned_data.get("job_country")
    model_country = _normalize_country_for_model(raw_country)
    company_name = cleaned_data.get("company_name")

    row = {
        "job_title_clean": _clean_text(cleaned_data.get("job_title_short")),
        # Used by the latest pipeline (see ModelsLoader) via a text/vectorizer transformer.
        "company_norm": _clean_text(company_name) or "unknown",
        "job_schedule_type_clean": _normalize_schedule_type_for_model(cleaned_data.get("job_schedule_type")),
        "IsRemoteNum": 1 if cleaned_data.get("job_work_from_home") == "Yes" else 0,
        "job_country": _clean_text(raw_country),

        # IMPORTANT: neutral defaults instead of always 0.0
        "company_target_smoothed": 0.5,
        "company_freq": 0.5,

        # Model expects country names here (despite the column name)
        "job_country_grouped": model_country,

        # Company size is not a job-seeker input in the UI; keep it static for inference.
        # Must match one of the categories seen during training.
        "company_size": "Medium",
    }

    for c in REQUIRED_COLUMNS:
        row.setdefault(c, 0)

    return pd.DataFrame([row], columns=REQUIRED_COLUMNS)
