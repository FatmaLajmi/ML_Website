"""
Remote Work Prediction Module
Predicts remote work eligibility based on job characteristics
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class RemoteWorkPredictor:
    """Remote work eligibility prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('remote_work')
    
    def predict(self, input_data):
        """
        Predict remote work eligibility
        Args:
            input_data: Dictionary with keys: job_title, industry, company_size
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_remote_work_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Remote work prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction (binary: remote or not)
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0] if hasattr(self.model, 'predict_proba') else None
            
            result = format_prediction_result(
                prediction={
                    'is_remote_eligible': bool(prediction),
                    'confidence': float(probability[1]) if probability is not None else None
                },
                model_type='remote_work'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'job_title': input_data['job_title'],
            'industry': input_data['industry'],
            'company_size': input_data['company_size']
        })
        
        return features


# Global predictor instance
remote_work_predictor = RemoteWorkPredictor()
