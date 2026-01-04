from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CampaignConversionPredictionForm
from .models import CampaignPrediction
from ml_models.predictors.campaign_conversion_predictor import campaign_conversion_predictor


@login_required
def campaign_conversion_view(request):
    """View for marketing campaign conversion predictions"""
    prediction_result = None
    
    if request.method == 'POST':
        form = CampaignConversionPredictionForm(request.POST)
        
        if form.is_valid():
            # Prepare input data
            input_data = {
                'campaign_type': form.cleaned_data['campaign_type'],
                'target_audience': form.cleaned_data['target_audience'],
                'duration': form.cleaned_data['duration'],
                'channel_used': form.cleaned_data['channel_used'],
                'language': form.cleaned_data['language'],
                'customer_segment': form.cleaned_data['customer_segment'],
            }
            
            # Make prediction
            prediction_result = campaign_conversion_predictor.predict(input_data)
            
            # Save prediction if successful
            if prediction_result.get('success'):
                try:
                    CampaignPrediction.objects.create(
                        user=request.user,
                        company='N/A',  # No longer collected
                        campaign_type=input_data['campaign_type'],
                        target_audience=input_data['target_audience'],
                        duration=input_data['duration'],
                        channel_used=input_data['channel_used'],
                        location='N/A',  # No longer collected
                        language=input_data['language'],
                        customer_segment=input_data['customer_segment'],
                        prediction=prediction_result['prediction'],
                        confidence=prediction_result['confidence'],
                        probability_high=prediction_result['probability_high'],
                        probability_low=prediction_result['probability_low']
                    )
                    messages.success(request, 'Campaign prediction completed and saved!')
                except Exception as e:
                    messages.warning(request, f'Prediction completed but could not save: {str(e)}')
            elif 'error' in prediction_result:
                messages.error(request, prediction_result['error'])
    else:
        form = CampaignConversionPredictionForm()
    
    # Get user's previous predictions
    previous_predictions = CampaignPrediction.objects.filter(user=request.user)[:10] if request.user.is_authenticated else []
    
    context = {
        'form': form,
        'prediction_result': prediction_result,
        'previous_predictions': previous_predictions,
    }
    
    return render(request, 'predictions/campaign_prediction.html', context)


@login_required
def job_seeker_predictions_view(request):
    """Placeholder view for job seeker predictions"""
    return render(request, 'predictions/jobSeekersPredictions.html')


@login_required
def employer_predictions_view(request):
    """Placeholder view for employer predictions"""
    return render(request, 'predictions/employersPredictions.html')

