"""
ML Models Loader
Loads all .pkl model files once at startup for efficient prediction serving.
"""
import os
import pickle
from pathlib import Path


class ModelsLoader:
    """Singleton class to load and cache ML models"""
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelsLoader, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance
    
    def _load_models(self):
        """Load all .pkl models from the models directory"""
        models_dir = Path(__file__).parent / 'models'
        
        model_files = {
            'salary': 'salary_model.pkl',
            'job_title': 'job_title_model.pkl',
            'remote_work': 'remote_work_model.pkl',
            'degree': 'degree_model.pkl',
            'benefits': 'benefits_model.pkl',
            'company_growth': 'company_growth_model.pkl',
            'revenue_growth': 'revenue_growth_model.pkl',
            'campaign_conversion': 'campaign_conversion_model.pkl',
        }
        
        for model_name, filename in model_files.items():
            model_path = models_dir / filename
            if model_path.exists():
                try:
                    with open(model_path, 'rb') as f:
                        self._models[model_name] = pickle.load(f)
                    print(f"Loaded model: {model_name}")
                except Exception as e:
                    print(f"Error loading {model_name}: {e}")
            else:
                print(f"Model file not found: {filename}")
    
    def get_model(self, model_name):
        """Retrieve a loaded model by name"""
        return self._models.get(model_name)
    
    def is_model_loaded(self, model_name):
        """Check if a model is loaded"""
        return model_name in self._models


# Initialize the models loader
models_loader = ModelsLoader()
