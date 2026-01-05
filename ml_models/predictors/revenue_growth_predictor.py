"""
Revenue Growth Prediction Module
Predicts company revenue growth
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class RevenueGrowthPredictor:
    """Revenue growth prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('revenue_growth')
    
    def predict(self, input_data):
        """
        Predict revenue growth
        Args:
            input_data: Dictionary with keys: company_name, current_revenue, industry, market_share
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_revenue_growth_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Revenue growth prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Calculate projected revenue
            current_revenue = float(input_data['current_revenue'])
            growth_rate = float(prediction)
            projected_revenue = current_revenue * (1 + growth_rate / 100)
            
            result = format_prediction_result(
                prediction={
                    'growth_rate_percent': growth_rate,
                    'current_revenue': current_revenue,
                    'projected_revenue': projected_revenue,
                    'revenue_increase': projected_revenue - current_revenue
                },
                model_type='revenue_growth'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'company_name': input_data['company_name'],
            'current_revenue': input_data['current_revenue'],
            'industry': input_data['industry'],
            'market_share': input_data['market_share']
        })
        
        return features


# Global predictor instance
revenue_growth_predictor = RevenueGrowthPredictor()
