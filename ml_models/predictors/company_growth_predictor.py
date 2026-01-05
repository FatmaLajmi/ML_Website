"""
Company Revenue Growth Predictor
Predicts revenue growth percentage for employers using LightGBM pipeline
"""
import pickle
import pandas as pd
import numpy as np
from pathlib import Path


class CompanyGrowthPredictor:
    """Predicts company revenue growth percentage"""
    
    def __init__(self):
        """Load the LightGBM pipeline and features"""
        self.pipeline = None
        self.features = None
        self._load_model()
    
    def _load_model(self):
        """Load the LightGBM pipeline and feature list"""
        try:
            models_dir = Path(__file__).parent.parent / 'models'
            pipeline_path = models_dir / 'growth_lgbm_pipeline(jojo).pkl'
            features_path = models_dir / 'model_features(jojo).pkl'
            
            if pipeline_path.exists() and features_path.exists():
                # Try loading with different pickle protocols for compatibility
                try:
                    with open(pipeline_path, 'rb') as f:
                        self.pipeline = pickle.load(f, encoding='latin1')
                except Exception as e1:
                    print(f"First attempt failed: {e1}")
                    try:
                        import joblib
                        self.pipeline = joblib.load(pipeline_path)
                    except Exception as e2:
                        print(f"Joblib attempt failed: {e2}")
                        # Try one more time with pickle protocol 4
                        with open(pipeline_path, 'rb') as f:
                            self.pipeline = pickle.load(f, fix_imports=True, encoding='bytes')
                
                with open(features_path, 'rb') as f:
                    self.features = pickle.load(f)
                print(f"✓ Company growth model loaded with {len(self.features)} features: {self.features}")
            else:
                print(f"✗ Model files not found at {models_dir}")
                if not pipeline_path.exists():
                    print(f"  Missing: {pipeline_path}")
                if not features_path.exists():
                    print(f"  Missing: {features_path}")
        except Exception as e:
            print(f"✗ Error loading company growth model: {e}")
            import traceback
            traceback.print_exc()
    
    def predict(self, input_data):
        """
        Predict company revenue growth percentage
        Args:
            input_data: Dictionary with keys: workers, previous_workers, revenue, delta_workers, founded, industry
        Returns:
            Dictionary with prediction results
        """
        # Check if model is loaded
        if self.pipeline is None or self.features is None:
            return {
                'success': False,
                'error': 'Company growth prediction model is not available'
            }
        
        try:
            # Validate and convert inputs
            workers = float(input_data.get('workers', 0))
            previous_workers = float(input_data.get('previous_workers', 0))
            revenue = float(input_data.get('revenue', 0))
            delta_workers = float(input_data.get('delta_workers', 0))
            founded = int(input_data.get('founded', 2000))
            industry = input_data.get('industry', '')
            
            # Validate inputs
            if workers <= 0 or previous_workers <= 0 or revenue <= 0:
                return {
                    'success': False,
                    'error': 'Workers, previous workers, and revenue must be positive numbers'
                }
            
            # Engineer features
            features_df = self._engineer_features(
                workers, previous_workers, revenue, delta_workers, founded, industry
            )
            
            # Make prediction (log-transformed)
            prediction_log = self.pipeline.predict(features_df)[0]
            
            # Inverse transform to get actual growth percentage
            growth_percentage = np.sign(prediction_log) * np.expm1(np.abs(prediction_log))
            
            # SANITY CHECK: If workforce is declining significantly, cap the growth prediction
            # This is a temporary fix until the model is retrained
            workforce_change_pct = (workers - previous_workers) / previous_workers if previous_workers > 0 else 0
            
            if workforce_change_pct < -0.1:  # More than 10% workforce decline
                # Cap growth at 0 or make it proportional to workforce decline
                max_growth = max(0, workforce_change_pct * 50)  # Scale down
                if growth_percentage > max_growth:
                    print(f"WARNING: Model predicted {growth_percentage:.2f}% growth with {workforce_change_pct*100:.1f}% workforce decline.")
                    print(f"         Capping prediction to {max_growth:.2f}% (model needs retraining)")
                    growth_percentage = max_growth
            
            # Categorize growth
            interpretation = self._categorize_growth(growth_percentage)
            
            return {
                'success': True,
                'growth_percentage': float(growth_percentage),
                'growth_percentage_formatted': f"{growth_percentage:.2f}%",
                'interpretation': interpretation
            }
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }
    
    def _engineer_features(self, workers, previous_workers, revenue, delta_workers, founded, industry):
        """Engineer features matching training data"""
        from datetime import datetime
        
        # Ensure all numeric inputs are floats
        workers = float(workers)
        previous_workers = float(previous_workers)
        revenue = float(revenue)
        delta_workers = float(delta_workers)
        founded = int(founded)
        
        # Calculate InitialRevenue (revenue at previous period based on growth rate assumption)
        # Assuming revenue grew proportionally with workers
        if workers > 0:
            revenue_per_worker = revenue / workers
            initial_revenue = revenue_per_worker * previous_workers
        else:
            initial_revenue = revenue
        
        # Calculate logarithmic transformations (adding small epsilon to avoid log(0))
        epsilon = 1e-10
        workers_log = float(np.log1p(workers + epsilon))
        rev_log = float(np.log1p(revenue + epsilon))
        init_log = float(np.log1p(initial_revenue + epsilon))
        
        # Calculate worker growth ratio
        if previous_workers > 0:
            worker_growth = float((workers - previous_workers) / previous_workers)
        else:
            worker_growth = 0.0
        
        # Calculate company age
        current_year = datetime.now().year
        age = int(current_year - founded)
        
        # Keep industry as string for the pipeline's OneHotEncoder
        # Determine if industry is in top category - but pass the actual string
        industry_top = industry if industry else 'Other'
        
        # Create DataFrame with engineered features in the correct order
        # Note: industry_top should be a STRING for the OneHotEncoder in the pipeline
        features_dict = {
            'workers': float(workers),
            'previous_workers': float(previous_workers),
            'InitialRevenue': float(initial_revenue),
            'workers_log': float(workers_log),
            'rev_log': float(rev_log),
            'init_log': float(init_log),
            'worker_growth': float(worker_growth),
            'age': float(age),
            'industry_top': industry_top  # Keep as string for OneHotEncoder
        }
        
        # Create DataFrame - do NOT force dtype for industry_top (it's categorical)
        features_df = pd.DataFrame([features_dict])
        
        # Reorder columns to match training features
        if self.features:
            features_df = features_df[self.features]
        
        # Convert numeric columns to float64, but keep industry_top as object/string
        numeric_cols = ['workers', 'previous_workers', 'InitialRevenue', 'workers_log', 
                       'rev_log', 'init_log', 'worker_growth', 'age']
        for col in numeric_cols:
            if col in features_df.columns:
                features_df[col] = features_df[col].astype(np.float64)
        
        return features_df
    
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
