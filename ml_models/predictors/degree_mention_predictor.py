"""
Degree Mention Predictor
Predicts whether a job posting mentions a degree requirement
Target: job_no_degree_mention
  - 1 = No degree mentioned (No Degree Required)
  - 0 = Degree mentioned (Degree Required)
"""
import pickle
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder


class DegreeMentionPredictor:
    """Predicts if a job posting mentions degree requirements"""
    
    def __init__(self):
        """Load the XGBoost model and features"""
        self.model = None
        self.features = None
        self._load_model()
    
    def _load_model(self):
        """Load the XGBoost classifier and feature list"""
        try:
            models_dir = Path(__file__).parent.parent / 'models'
            model_path = models_dir / 'xgb_classifier_model(jojo).pkl'
            features_path = models_dir / 'xgb_features(jojo).pkl'
            
            if model_path.exists() and features_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                print(f"✓ Degree mention model loaded with {len(self.features)} features: {self.features}")
            else:
                print(f"✗ Model files not found at {models_dir}")
        except Exception as e:
            print(f"✗ Error loading degree mention model: {e}")
            import traceback
            traceback.print_exc()
    
    def predict(self, input_data):
        """
        Predict if job mentions degree requirement
        
        Args:
            input_data: dict with keys:
                - skill_count (int)
                - job_title_short (str)
                - job_via (str)
                - company_name (str, optional)
                - job_country (str, optional)
                - search_location (str, optional)
        
        Returns:
            dict with keys:
                - success (bool)
                - prediction (str): "Degree Required" or "No Degree Required"
                - degree_mentioned (bool)
                - confidence (str): percentage
        """
        # Validate input
        errors = self._validate_input(input_data)
        if errors:
            return {'success': False, 'error': ', '.join(errors)}
        
        # Check model loaded
        if self.model is None or self.features is None:
            return {'success': False, 'error': 'Model not available'}
        
        try:
            # Prepare features
            features_df = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features_df)[0]
            
            # Get confidence
            try:
                probabilities = self.model.predict_proba(features_df)[0]
                confidence = max(probabilities) * 100
            except:
                confidence = None
            
            # Interpret result
            # After testing, the model appears to predict:
            # prediction == 1 means "degree IS required/mentioned"
            # prediction == 0 means "NO degree required/mentioned"
            degree_mentioned = (prediction == 1)
            result_text = "Degree Required" if degree_mentioned else "No Degree Required"
            
            return {
                'success': True,
                'prediction': result_text,
                'degree_mentioned': degree_mentioned,
                'confidence': f'{confidence:.1f}%' if confidence else 'N/A',
                'raw_prediction': int(prediction)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def _validate_input(self, input_data):
        """Validate required fields"""
        errors = []
        
        # Required fields
        required = ['skill_count', 'job_title_short', 'job_via']
        for field in required:
            if field not in input_data or not input_data[field]:
                errors.append(f'{field.replace("_", " ").title()} is required')
        
        # Validate skill_count is numeric
        if 'skill_count' in input_data:
            try:
                int(input_data['skill_count'])
            except (ValueError, TypeError):
                errors.append('Skill count must be a number')
        
        return errors
    
    def _prepare_features(self, input_data):
        """
        Prepare feature DataFrame with proper encoding
        
        Args:
            input_data: dict with feature values
        
        Returns:
            pandas DataFrame ready for prediction
        """
        # Build feature dictionary with defaults for optional fields
        feature_dict = {
            'skill_count': int(input_data['skill_count']),
            'job_title_short': str(input_data.get('job_title_short', '')),
            'job_via': str(input_data.get('job_via', '')),
            'company_name': str(input_data.get('company_name', 'Unknown')),
            'job_country': str(input_data.get('job_country', 'Unknown')),
            'search_location': str(input_data.get('search_location', 'Unknown'))
        }
        
        # Create DataFrame in correct feature order
        df = pd.DataFrame([feature_dict], columns=self.features)
        
        # Encode categorical features to numeric
        categorical_cols = ['job_title_short', 'job_via', 'company_name', 
                           'job_country', 'search_location']
        
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
        
        return df


# Singleton instance
degree_mention_predictor = DegreeMentionPredictor()
