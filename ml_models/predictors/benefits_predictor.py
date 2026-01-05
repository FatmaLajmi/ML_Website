"""
Benefits Prediction Module
Predicts likely benefits package for a job
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class BenefitsPredictor:
    """Benefits package prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('benefits')
    
    def predict(self, input_data):
        """
        Predict benefits package
        Args:
            input_data: Dictionary with keys: job_title, company_size, location
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_benefits_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Benefits prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)
            
            result = format_prediction_result(
                prediction={
                    'predicted_benefits': prediction.tolist() if hasattr(prediction, 'tolist') else list(prediction)
                },
                model_type='benefits'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'job_title': input_data['job_title'],
            'company_size': input_data['company_size'],
            'location': input_data['location']
        })
        
        return features


# Global predictor instance
benefits_predictor = BenefitsPredictor()
