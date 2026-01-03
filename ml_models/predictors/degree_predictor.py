"""
Degree Requirement Prediction Module
Predicts required education level for a job
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class DegreePredictor:
    """Degree requirement prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('degree')
    
    def predict(self, input_data):
        """
        Predict required degree for a job
        Args:
            input_data: Dictionary with keys: job_title, industry, experience_years
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_degree_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Degree prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            result = format_prediction_result(
                prediction={
                    'required_degree': str(prediction)
                },
                model_type='degree'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'job_title': input_data['job_title'],
            'industry': input_data['industry'],
            'experience_years': input_data['experience_years']
        })
        
        return features


# Global predictor instance
degree_predictor = DegreePredictor()
