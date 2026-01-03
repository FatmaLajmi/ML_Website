"""
Salary Prediction Module
Predicts salary based on job title, experience, education, and location
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result, calculate_confidence_interval


class SalaryPredictor:
    """Salary prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('salary')
    
    def predict(self, input_data):
        """
        Predict salary based on input features
        Args:
            input_data: Dictionary with keys: job_title, experience_years, education_level, location
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_salary_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Salary prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Calculate confidence interval
            lower, upper = calculate_confidence_interval(prediction)
            
            result = format_prediction_result(
                prediction={
                    'estimated_salary': float(prediction),
                    'range': {
                        'lower': float(lower),
                        'upper': float(upper)
                    }
                },
                model_type='salary'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        # This would be customized based on actual model training
        features = preprocessor.prepare_feature_dict({
            'job_title': input_data['job_title'],
            'experience_years': input_data['experience_years'],
            'education_level': input_data['education_level'],
            'location': input_data['location']
        })
        
        return features


# Global predictor instance
salary_predictor = SalaryPredictor()
