"""
Job Title Prediction Module
Predicts suitable job titles based on skills and experience
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class JobTitlePredictor:
    """Job title prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('job_title')
    
    def predict(self, input_data):
        """
        Predict job titles based on skills and experience
        Args:
            input_data: Dictionary with keys: skills, experience_years
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_job_title_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Job title prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction (could return top N job titles)
            prediction = self.model.predict(features)
            
            result = format_prediction_result(
                prediction={
                    'recommended_titles': prediction.tolist() if hasattr(prediction, 'tolist') else list(prediction)
                },
                model_type='job_title'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        skills_list = preprocessor.parse_skills(input_data['skills'])
        
        features = preprocessor.prepare_feature_dict({
            'skills': skills_list,
            'experience_years': input_data['experience_years']
        })
        
        return features


# Global predictor instance
job_title_predictor = JobTitlePredictor()
