"""
Health Insurance Prediction Module
Predicts whether a job posting offers health insurance (Yes/No)
"""
from ..models_loader import models_loader
from ..validators import validator
from ..utils import format_prediction_result
from ..preprocessing import prepare_health_insurance_features


class HealthInsurancePredictor:
    def __init__(self):
        self.model = models_loader.get_model('health_insurance')

    def predict(self, input_data):
        # Optional: add a validator method, or skip validation for now
        # errors = validator.validate_health_insurance_input(input_data)
        # if errors:
        #     return {'error': ', '.join(errors)}

        if self.model is None:
            return {'error': 'Health insurance prediction model is not available'}

        try:
            X = prepare_health_insurance_features(input_data)
            pred = self.model.predict(X)[0]

            proba = None
            if hasattr(self.model, "predict_proba"):
                proba = float(self.model.predict_proba(X)[0][1])

            pred_int = int(pred)

            label = "Has health insurance" if pred_int == 1 else "Don't have health insurance"

            return format_prediction_result(
                prediction={
                    "has_health_insurance": pred_int,
                    "has_health_insurance_label": label,
                    "probability_yes": proba,
                },
                model_type="health_insurance",
            )

        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}


health_insurance_predictor = HealthInsurancePredictor()