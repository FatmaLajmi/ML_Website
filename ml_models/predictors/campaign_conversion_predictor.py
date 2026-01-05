"""
Campaign Conversion Prediction Module
Predicts campaign conversion rates
"""
from ..models_loader import models_loader
from ..preprocessing import preprocessor
from ..validators import validator
from ..utils import format_prediction_result


class CampaignConversionPredictor:
    """Campaign conversion prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('campaign_conversion')
    
    def predict(self, input_data):
        """
        Predict campaign conversion rate
        Args:
            input_data: Dictionary with keys: campaign_name, budget, target_audience_size, duration_days
        Returns:
            Dictionary with prediction results
        """
        # Validate input
        errors = validator.validate_campaign_conversion_input(input_data)
        if errors:
            return {'error': ', '.join(errors)}
        
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Campaign conversion prediction model is not available'}
        
        try:
            # Preprocess input data
            features = self._prepare_features(input_data)
            
            # Make prediction
            conversion_rate = self.model.predict(features)[0]
            
            # Calculate expected conversions
            audience_size = int(input_data['target_audience_size'])
            expected_conversions = int(audience_size * conversion_rate / 100)
            
            # Calculate cost per conversion
            budget = float(input_data['budget'])
            cost_per_conversion = budget / expected_conversions if expected_conversions > 0 else 0
            
            result = format_prediction_result(
                prediction={
                    'conversion_rate_percent': float(conversion_rate),
                    'expected_conversions': expected_conversions,
                    'cost_per_conversion': cost_per_conversion,
                    'campaign_roi': self._calculate_roi(conversion_rate)
                },
                model_type='campaign_conversion'
            )
            
            return result
        
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """Prepare feature array for model input"""
        features = preprocessor.prepare_feature_dict({
            'campaign_name': input_data['campaign_name'],
            'budget': input_data['budget'],
            'target_audience_size': input_data['target_audience_size'],
            'duration_days': input_data['duration_days']
        })
        
        return features
    
    def _calculate_roi(self, conversion_rate):
        """Categorize ROI based on conversion rate"""
        if conversion_rate < 1:
            return "Poor"
        elif conversion_rate < 3:
            return "Fair"
        elif conversion_rate < 5:
            return "Good"
        elif conversion_rate < 10:
            return "Excellent"
        else:
            return "Outstanding"


# Global predictor instance
campaign_conversion_predictor = CampaignConversionPredictor()
