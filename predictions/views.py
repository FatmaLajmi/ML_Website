from django.shortcuts import render

from .forms import HealthInsuranceForm
from ml_models.predictors.health_insurance_predictor import health_insurance_predictor


def health_insurance_view(request):
    result = None

    if request.method == "POST":
        form = HealthInsuranceForm(request.POST)
        if form.is_valid():
            try:
                result = health_insurance_predictor.predict(form.cleaned_data)

                # Normalize result so template always works, even if predictor returns a raw value
                if not isinstance(result, dict):
                    result = {
                        "has_health_insurance_label": str(result),
                        "probability_yes": None,
                        "error": None,
                    }
                else:
                    # If predictor returned the formatted structure from utils.format_prediction_result,
                    # its useful values are under result['prediction']. Merge them to top-level for template.
                    pred = result.get('prediction') if isinstance(result.get('prediction'), dict) else {}
                    # top-level error/probability/label should prefer explicit top-level keys, then nested prediction
                    result['error'] = result.get('error') or pred.get('error') or None
                    result['probability_yes'] = result.get('probability_yes') if result.get('probability_yes') is not None else pred.get('probability_yes')
                    result['has_health_insurance'] = result.get('has_health_insurance') if result.get('has_health_insurance') is not None else pred.get('has_health_insurance')
                    result['has_health_insurance_label'] = result.get('has_health_insurance_label') if result.get('has_health_insurance_label') is not None else pred.get('has_health_insurance_label')

            except Exception as e:
                result = {
                    "error": f"Prediction failed: {e}",
                    "has_health_insurance_label": None,
                    "probability_yes": None,
                }
    else:
        form = HealthInsuranceForm()

    return render(request, "predictions/health_insurance.html", {"form": form, "result": result})