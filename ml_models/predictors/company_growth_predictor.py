"""
Company Growth Prediction Module
Predicts company growth trajectory
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class CompanyGrowthPredictor:
    """Company growth prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('company_growth')
    
    def predict(self, input_data):
        """
        Predict company growth
        Args:
            input_data: Dictionary with keys: company_name, industry, employee_count, years_in_business
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_company_growth_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Company growth prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            result = format_prediction_result(
                prediction={
                    'growth_rate': float(prediction),
                    'category': self._categorize_growth(prediction)
                },
                model_type='company_growth'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'company_name': input_data['company_name'],
            'industry': input_data['industry'],
            'employee_count': input_data['employee_count'],
            'years_in_business': input_data['years_in_business']
        })
        
        return features
    
    def _categorize_growth(self, growth_rate):
        """Categorize growth rate"""
        if growth_rate < 0:
            return "Declining"
        elif growth_rate < 5:
            return "Slow Growth"
        elif growth_rate < 15:
            return "Moderate Growth"
        elif growth_rate < 30:
            return "High Growth"
        else:
            return "Rapid Growth"


# Global predictor instance
company_growth_predictor = CompanyGrowthPredictor()
