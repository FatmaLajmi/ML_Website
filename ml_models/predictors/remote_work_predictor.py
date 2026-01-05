import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime

REQUIRED_FIELDS = [
    "job_title_short",
    "job_seniority",
    "job_country",
    "job_schedule_type",
    "text_block",
]

_MODEL = None

def _get_model():
    global _MODEL
    if _MODEL is None:
        model_path = Path(__file__).resolve().parent.parent / "models" / "remote_work_v3(eya).pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        _MODEL = joblib.load(model_path)
    return _MODEL


def validate_input(data):
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")


def _adjust_proba_by_text(proba: float, text_block: str) -> float:
    """
    Adjust probability based on remote-related keywords in text
    Model is biased toward on-site, so we boost remote if keywords are present
    """
    text_lower = str(text_block).lower()
    
    # Keywords indicating remote work
    remote_keywords = [
        "remote", "work from home", "wfh", "work anywhere", "flexible",
        "distributed team", "virtual", "telecommute", "home office",
        "anywhere in", "location independent", "fully remote"
    ]
    
    # Keywords indicating on-site
    onsite_keywords = [
        "on-site", "onsite", "in office", "office location", "headquarter",
        "in-person", "reporting to office", "must be on-site"
    ]
    
    # Count keywords
    remote_count = sum(1 for kw in remote_keywords if kw in text_lower)
    onsite_count = sum(1 for kw in onsite_keywords if kw in text_lower)
    
    # Boost probability if remote keywords are found
    if remote_count > 0:
        # Stronger boost: each keyword = 20% boost instead of 15%
        boost = min(0.5, remote_count * 0.20)
        proba = min(1.0, proba + boost)
    
    # Reduce probability if on-site keywords are found
    if onsite_count > 0:
        reduction = min(0.5, onsite_count * 0.25)
        proba = max(0.0, proba - reduction)
    
    return proba


def predict_remote_work(data: dict) -> dict:
    try:
        validate_input(data)
        model = _get_model()

        month = datetime.now().month
        quarter = (month - 1) // 3 + 1

        # Create DataFrame with exact column order expected by the model
        X = pd.DataFrame([{
            "job_title_short": str(data["job_title_short"]).strip(),
            "job_seniority": str(data["job_seniority"]).strip(),
            "job_country": str(data["job_country"]).strip(),
            "job_schedule_type": str(data["job_schedule_type"]).strip(),
            "job_via": "Unknown",
            "posted_month": int(month),
            "posted_quarter": int(quarter),
            "text_block": str(data["text_block"]).strip(),
        }])

        if not hasattr(model, "predict_proba"):
            raise AttributeError("Model does not support predict_proba")

        # The model pipeline handles encoding internally
        proba = float(model.predict_proba(X)[0, 1])
        
        # Adjust probability based on text content
        # Model is heavily biased toward on-site, so we need text analysis
        text_block = data.get("text_block", "")
        proba = _adjust_proba_by_text(proba, text_block)
        
        prediction = "Remote" if proba >= 0.5 else "On-site"

        return {
            "success": True,
            "prediction": prediction,
            "proba_remote": round(proba, 4),
            "proba_remote_pct": round(proba * 100, 2),
            "threshold": 0.5,
        }

    except FileNotFoundError as e:
        return {"success": False, "error": f"Model file not found: {str(e)}"}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        import traceback
        print(f"Remote work prediction error: {traceback.format_exc()}")
        return {"success": False, "error": f"Prediction failed: {str(e)}"}


class RemoteWorkPredictor:
    """Remote work prediction handler - compatible interface"""
    
    def predict(self, data: dict) -> dict:
        """Make prediction using predict_remote_work function"""
        return predict_remote_work(data)


# Global predictor instance for consistency with other predictors
remote_work_predictor = RemoteWorkPredictor()
