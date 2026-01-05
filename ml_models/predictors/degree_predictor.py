"""
Degree Requirement Prediction Module
Predicts whether a job posting requires a degree using XGBoost classifier
"""
import os
import pickle
import pandas as pd
from pathlib import Path


class DegreePredictor:
    """Degree requirement prediction handler using XGBoost"""
    
    def __init__(self):
        """Load the XGBoost model and feature list"""
        self.model = None
        self.features = None
        self._load_model()
    
    def _load_model(self):
        """Load the XGBoost classifier model and features from pkl files"""
        try:
            models_dir = Path(__file__).parent.parent / 'models'
            model_path = models_dir / 'xgb_classifier_model(jojo).pkl'
            features_path = models_dir / 'xgb_features(jojo).pkl'
            
            print(f"Looking for model in: {models_dir}")
            print(f"Model path: {model_path}")
            print(f"Features path: {features_path}")
            print(f"Model exists: {model_path.exists()}")
            print(f"Features exists: {features_path.exists()}")
            
            if model_path.exists() and features_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                print(f"Degree prediction model loaded successfully with {len(self.features)} features")
            else:
                print(f"Model files not found at {models_dir}")
                if not model_path.exists():
                    print(f"Missing: {model_path}")
                if not features_path.exists():
                    print(f"Missing: {features_path}")
        except Exception as e:
            print(f"Error loading degree prediction model: {e}")
            import traceback
            traceback.print_exc()
    
    def predict(self, input_data):
        """
        Predict whether a job requires a degree
        
        Args:
            input_data: Dictionary with keys: skill_count, job_title_short, job_via, 
                       company_name, job_country, search_location
        
        Returns:
            Dictionary with prediction results
        """
        # Reload model if not loaded (can happen after Django auto-reload)
        if self.model is None or self.features is None:
            print("Model not loaded, attempting to reload...")
            self._load_model()
        
        # Check if model is loaded
        if self.model is None or self.features is None:
            return {
                'error': 'Degree prediction model is not available. Please check model files.',
                'success': False
            }
        
        # Validate input
        errors = self._validate_input(input_data)
        if errors:
            return {'error': ', '.join(errors), 'success': False}
        
        try:
            # Prepare features for prediction
            features_df = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features_df)[0]
            
            # Get prediction probability if available
            try:
                probability = self.model.predict_proba(features_df)[0]
                confidence = max(probability) * 100
            except:
                confidence = None
            
            # Format result
            result = {
                'success': True,
                'prediction': 'Degree Required' if prediction == 1 else 'No Degree Required',
                'degree_required': bool(prediction),
                'confidence': f'{confidence:.1f}%' if confidence else 'N/A'
            }
            
            return result
        
        except Exception as e:
            return {
                'error': f'Prediction failed: {str(e)}',
                'success': False
            }
    
    def _validate_input(self, input_data):
        """Validate input data"""
        errors = []
        required_fields = ['skill_count', 'job_title_short', 'job_via', 
                          'company_name', 'job_country', 'search_location']
        
        for field in required_fields:
            if field not in input_data or input_data[field] is None or input_data[field] == '':
                errors.append(f'{field.replace("_", " ").title()} is required')
        
        # Validate skill_count is a number
        if 'skill_count' in input_data:
            try:
                int(input_data['skill_count'])
            except (ValueError, TypeError):
                errors.append('Skill count must be a valid number')
        
        return errors
    
    def _prepare_features(self, input_data):
        """
        Prepare feature DataFrame for model input
        
        Args:
            input_data: Dictionary with feature values
            
        Returns:
            pandas DataFrame with features in correct order
        """
        from sklearn.preprocessing import LabelEncoder
        
        # Create a dictionary with all features
        feature_dict = {
            'skill_count': int(input_data['skill_count']),
            'job_title_short': str(input_data['job_title_short']),
            'job_via': str(input_data['job_via']),
            'company_name': str(input_data['company_name']),
            'job_country': str(input_data['job_country']),
            'search_location': str(input_data['search_location'])
        }
        
        # Create DataFrame with features in the correct order
        features_df = pd.DataFrame([feature_dict], columns=self.features)
        
        # Encode categorical features to numeric
        categorical_columns = ['job_title_short', 'job_via', 'company_name', 'job_country', 'search_location']
        
        for col in categorical_columns:
            if col in features_df.columns:
                le = LabelEncoder()
                # Fit and transform in one step
                features_df[col] = le.fit_transform(features_df[col].astype(str))
        
        return features_df


# Global predictor instance
degree_predictor = DegreePredictor()
