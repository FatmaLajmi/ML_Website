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
