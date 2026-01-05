"""
XGBoost Company Growth Predictor
Predicts company growth using XGBoost model with dynamic feature encoding
"""
import pickle
import numpy as np
from pathlib import Path


class XGBoostGrowthPredictor:
    """Predicts company growth using XGBoost model"""
    
    def __init__(self):
        """Load the XGBoost model and feature list"""
        self.model = None
        self.features = None
        self.industries = []
        self.states = []
        self._load_model()
    
    def _load_model(self):
        """Load the XGBoost model and feature list"""
        try:
            models_dir = Path(__file__).parent.parent / 'models'
            model_path = models_dir / 'xgboost_growth_model.pkl'
            features_path = models_dir / 'model_features.pkl'
            
            # Define the exact industries used in training
            self.industries = [
                'Advertising & Marketing',
                'Business Products & Services',
                'Computer Hardware',
                'Construction',
                'Consumer Products & Services',
                'Education',
                'Energy',
                'Engineering',
                'Environmental Services',
                'Financial Services',
                'Food & Beverage',
                'Government Services',
                'Health',
                'Human Resources',
                'Insurance',
                'IT Management',
                'IT Services',
                'IT System Development',
                'Logistics & Transportation',
                'Manufacturing',
                'Media',
                'Real Estate',
                'Retail',
                'Security',
                'Software',
                'Telecommunications',
                'Travel & Hospitality'
            ]
            
            if model_path.exists() and features_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                
                print(f"✓ XGBoost growth model loaded with {len(self.features)} features")
                # Extract state options from feature names
                self.states = [f.replace('State_', '') for f in self.features if f.startswith('State_')]
                print(f"  - Industries: {len(self.industries)} options")
                print(f"  - States: {len(self.states)} options")
            else:
                print(f"✗ XGBoost growth model files not found at {models_dir}")
                if not model_path.exists():
                    print(f"  Missing: {model_path}")
                if not features_path.exists():
                    print(f"  Missing: {features_path}")
        except Exception as e:
            print(f"✗ Error loading XGBoost growth model: {e}")
            import traceback
            traceback.print_exc()
    
    def predict(self, input_data):
        """
        Predict company growth
        Args:
            input_data: Dictionary with keys:
                - years_on_list: Number of years company has been on the list
                - company_age: Age of the company in years
                - hiring_growth: Hiring growth rate (decimal/float)
                - industry: Industry name (must match one from model)
                - state: State code (must match one from model)
        Returns:
            Dictionary with prediction results
        """
        # Check if model is loaded
        if self.model is None or self.features is None:
            return {
                'success': False,
                'error': 'XGBoost growth prediction model is not available'
            }
        
        try:
            # Validate and extract inputs
            years_on_list = float(input_data.get('years_on_list', 0))
            company_age = float(input_data.get('company_age', 0))
            hiring_growth = float(input_data.get('hiring_growth', 0))
            industry = input_data.get('industry', '')
            state = input_data.get('state', '')
            
            # Validate inputs
            if years_on_list < 0 or company_age < 0:
                return {
                    'success': False,
                    'error': 'Years on list and company age must be non-negative'
                }
            
            if not industry or not state:
                return {
                    'success': False,
                    'error': 'Industry and state are required'
                }
            
            # Construct feature vector dynamically
            feature_vector = self._construct_feature_vector(
                years_on_list, company_age, hiring_growth, industry, state
            )
            
            # Make prediction - classification model outputs class label
            prediction = self.model.predict(feature_vector)[0]
            
            # The model outputs a class label (likely 0 or 1, or category name)
            # Interpret the prediction
            growth_category = self._interpret_prediction(prediction)
            
            return {
                'success': True,
                'growth_category': growth_category,
                'raw_prediction': str(prediction),
                'input_summary': {
                    'years_on_list': years_on_list,
                    'company_age': company_age,
                    'hiring_growth': hiring_growth,
                    'industry': industry,
                    'state': state
                }
            }
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def _construct_feature_vector(self, years_on_list, company_age, hiring_growth, industry, state):
        """
        Dynamically construct feature vector matching the model's expected input
        """
        # Initialize feature vector with zeros
        feature_vector = np.zeros(len(self.features))
        
        # Map features by name
        for idx, feature_name in enumerate(self.features):
            if feature_name == 'YearsOnList':
                feature_vector[idx] = years_on_list
            elif feature_name == 'CompanyAge':
                feature_vector[idx] = company_age
            elif feature_name == 'HiringGrowth':
                feature_vector[idx] = hiring_growth
            elif feature_name == f'industry_{industry}':
                feature_vector[idx] = 1  # One-hot encode industry
            elif feature_name == f'State_{state}':
                feature_vector[idx] = 1  # One-hot encode state
        
        # Reshape for model input (1 sample, n features)
        return feature_vector.reshape(1, -1)
    
    def _interpret_prediction(self, prediction):
        """
        Interpret the classification prediction
        The model likely outputs 0 or 1, or similar class labels
        Map these to meaningful categories
        """
        # Convert prediction to string for comparison
        pred_str = str(prediction).lower()
        
        # Check for various possible output formats
        if prediction == 1 or pred_str in ['1', '1.0', 'high', 'high growth']:
            return "High Growth"
        elif prediction == 0 or pred_str in ['0', '0.0', 'low', 'low growth']:
            return "Low Growth"
        else:
            # If we get something unexpected, return it as-is
            return f"Growth Class: {prediction}"
    
    def get_industry_choices(self):
        """Get list of valid industry choices"""
        if self.industries:
            return [(ind, ind) for ind in sorted(self.industries)]
        return []
    
    def get_state_choices(self):
        """Get list of valid state choices"""
        if self.states:
            return [(state, state) for state in sorted(self.states)]
        return []


# Global predictor instance
xgboost_growth_predictor = XGBoostGrowthPredictor()
