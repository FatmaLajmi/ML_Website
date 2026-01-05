"""
ML Models Loader
Loads all .pkl model files once at startup for efficient prediction serving.
"""
import os
import pickle
from pathlib import Path
import traceback
try:
    import joblib
except Exception:
    joblib = None
try:
    import cloudpickle
except Exception:
    cloudpickle = None


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

        # Health insurance model:
        # Prefer a stable, short filename if present, otherwise fall back to the newest timestamped export.
        health_preferred = models_dir / "health_insurance_best.pkl"
        if health_preferred.exists():
            health_filename = health_preferred.name
        else:
            health_candidates = sorted(
                models_dir.glob("best_xgb_insurance_model_*.pkl"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            health_filename = health_candidates[0].name if health_candidates else "health_insurance_pipeline.pkl"
        
        model_files = {
            "health_insurance": health_filename,
            'salary': 'salary_model.pkl',
            'job_title': 'job_title_model.pkl',
            'remote_work': 'remote_work_model.pkl',
            'degree': 'degree_model.pkl',
            'benefits': 'benefits_model.pkl',
            'company_growth': 'company_growth_model.pkl',
            'revenue_growth': 'revenue_growth_model.pkl',
            'campaign_conversion': 'best_random_forest_model.pkl',
            'campaign_scaler': 'campaign_scaler.pkl',
        }
        
        for model_name, filename in model_files.items():
            model_path = models_dir / filename
            if not model_path.exists():
                print(f"Model file not found: {filename}")
                continue

            loaded = False
            # Try pickle first
            try:
                with open(model_path, 'rb') as f:
                    self._models[model_name] = pickle.load(f)
                print(f"Loaded model with pickle: {model_name} ({filename})")
                loaded = True
            except Exception:
                print(f"pickle.load failed for {model_name}, trying joblib/cloudpickle...")
                traceback.print_exc()

            # Try joblib if pickle failed
            if not loaded and joblib is not None:
                try:
                    self._models[model_name] = joblib.load(model_path)
                    print(f"Loaded model with joblib: {model_name} ({filename})")
                    loaded = True
                except Exception:
                    print(f"joblib.load failed for {model_name}...")
                    traceback.print_exc()

            # Try cloudpickle as last resort
            if not loaded and cloudpickle is not None:
                try:
                    with open(model_path, 'rb') as f:
                        self._models[model_name] = cloudpickle.load(f)
                    print(f"Loaded model with cloudpickle: {model_name} ({filename})")
                    loaded = True
                except Exception:
                    print(f"cloudpickle.load failed for {model_name}...")
                    traceback.print_exc()

            if not loaded:
                print(f"Failed to load model: {model_name}")
                        # Try loading with different encodings for compatibility
                        try:
                            self._models[model_name] = pickle.load(f)
                        except:
                            f.seek(0)
                            self._models[model_name] = pickle.load(f, encoding='latin1')
                    print(f"Loaded model: {model_name}")
                except Exception as e:
                    print(f"Error loading {model_name}: {e}")
                    # Try with joblib as fallback
                    try:
                        import joblib
                        self._models[model_name] = joblib.load(model_path)
                        print(f"Loaded model with joblib: {model_name}")
                    except Exception as e2:
                        print(f"Joblib also failed for {model_name}: {e2}")
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
