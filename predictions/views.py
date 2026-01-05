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
                'company': form.cleaned_data['company'],
                'campaign_type': form.cleaned_data['campaign_type'],
                'target_audience': form.cleaned_data['target_audience'],
                'duration': form.cleaned_data['duration'],
                'channel_used': form.cleaned_data['channel_used'],
                'location': form.cleaned_data['location'],
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
                        company=input_data['company'],
                        campaign_type=input_data['campaign_type'],
                        target_audience=input_data['target_audience'],
                        duration=input_data['duration'],
                        channel_used=input_data['channel_used'],
                        location=input_data['location'],
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
from django.shortcuts import render
from django.contrib import messages
from .forms import (
    SalaryPredictionForm, JobTitlePredictionForm, RemoteWorkPredictionForm,
    DegreePredictionForm, BenefitsPredictionForm, CompanyGrowthPredictionForm,
    RevenueGrowthPredictionForm, CampaignConversionPredictionForm, XGBoostGrowthPredictionForm
)
import pickle
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def degree_mention_view(request):
    """
    Dedicated view for degree mention prediction ONLY
    Uses xgb_classifier_model(jojo).pkl
    """
    context = {}
    
    if request.method == 'POST':
        # Get form data
        input_data = {
            'skill_count': request.POST.get('skill_count'),
            'job_title_short': request.POST.get('job_title_short'),
            'job_via': request.POST.get('job_via'),
            'company_name': request.POST.get('company_name', 'Unknown'),
            'job_country': request.POST.get('job_country', 'Unknown'),
            'search_location': request.POST.get('search_location', 'Unknown'),
        }
        
        # Import and use the degree mention predictor
        from ml_models.predictors.degree_mention_predictor import degree_mention_predictor
        
        # Make prediction
        result = degree_mention_predictor.predict(input_data)
        
        # Add result to context
        if result.get('success'):
            context['result'] = result
            messages.success(request, f"Prediction: {result['prediction']}")
        else:
            messages.error(request, result.get('error', 'Prediction failed'))
        
        # Keep form data for display
        context['form_data'] = input_data
    
    return render(request, 'predictions/degree_mention.html', context)


def job_seeker_predictions_view(request):
    """View for job seeker predictions including degree requirement prediction"""
    context = {
        'salary_form': SalaryPredictionForm(),
        'job_title_form': JobTitlePredictionForm(),
        'remote_work_form': RemoteWorkPredictionForm(),
        'degree_form': DegreePredictionForm(),
        'benefits_form': BenefitsPredictionForm(),
    }
    
    # Handle degree prediction form submission
    if request.method == 'POST':
        prediction_type = request.POST.get('prediction_type')
        
        if prediction_type == 'degree':
            degree_form = DegreePredictionForm(request.POST)
            
            if degree_form.is_valid():
                # Extract form data
                input_data = {
                    'skill_count': degree_form.cleaned_data['skill_count'],
                    'job_title_short': degree_form.cleaned_data['job_title_short'],
                    'job_via': degree_form.cleaned_data['job_via'],
                    'company_name': degree_form.cleaned_data['company_name'],
                    'job_country': degree_form.cleaned_data['job_country'],
                    'search_location': degree_form.cleaned_data['search_location'],
                }
                
                # Use degree mention predictor
                from ml_models.predictors.degree_mention_predictor import degree_mention_predictor
                result = degree_mention_predictor.predict(input_data)
                
                # Add result to context
                if result.get('success'):
                    context['degree_result'] = result
                    messages.success(request, f"Prediction complete: {result['prediction']}")
                else:
                    messages.error(request, result.get('error', 'Prediction failed'))
                
                # Keep the submitted form data
                context['degree_form'] = degree_form
            else:
                messages.error(request, 'Please correct the errors in the form')
                context['degree_form'] = degree_form
        
        # Handle other prediction types here (salary, job_title, etc.)
        # TODO: Add handlers for other prediction types
    
    return render(request, 'predictions/jobSeekersPredictions.html', context)


def employer_predictions_view(request):
    """View for employer predictions"""
    context = {
        'company_growth_form': CompanyGrowthPredictionForm(),
        'revenue_growth_form': RevenueGrowthPredictionForm(),
        'campaign_conversion_form': CampaignConversionPredictionForm(),
        'xgboost_growth_form': XGBoostGrowthPredictionForm(),
    }
    
    if request.method == 'POST':
        prediction_type = request.POST.get('prediction_type', '')
        
        if prediction_type == 'growth':
            # Handle company growth prediction
            try:
                workers_input = request.POST.get('workers', '').strip()
                prev_workers_input = request.POST.get('previous_workers', '').strip()
                revenue_input = request.POST.get('revenue', '').strip()
                delta_workers_input = request.POST.get('delta_workers', '').strip()
                founded_input = request.POST.get('founded', '').strip()
                industry_input = request.POST.get('industry', '').strip()
                
                # Validate required fields
                if not all([workers_input, prev_workers_input, revenue_input]):
                    messages.error(request, 'Please fill in all required fields')
                    # Preserve form data for re-display
                    context['growth_form_data'] = {
                        'workers': workers_input,
                        'previous_workers': prev_workers_input,
                        'revenue': revenue_input,
                        'delta_workers': delta_workers_input,
                        'founded': founded_input,
                        'industry': industry_input,
                    }
                    return render(request, 'predictions/employersPredictions.html', context)
                
                # Calculate delta if not provided
                if not delta_workers_input:
                    delta_workers_input = str(float(workers_input) - float(prev_workers_input))
                
                # Default founded year if not provided
                if not founded_input:
                    founded_input = '2010'
                
                input_data = {
                    'workers': float(workers_input),
                    'previous_workers': float(prev_workers_input),
                    'revenue': float(revenue_input),
                    'delta_workers': float(delta_workers_input),
                    'founded': int(founded_input),
                    'industry': industry_input if industry_input else 'Other',
                }
                
                # Import and use the company growth predictor
                from ml_models.predictors.company_growth_predictor import company_growth_predictor
                
                # Make prediction
                result = company_growth_predictor.predict(input_data)
                
                if result.get('success'):
                    context['growth_result'] = result
                    messages.success(request, f"Predicted Growth: {result['growth_percentage_formatted']}")
                    print(f"DEBUG: Prediction successful! Result: {result}")
                    print(f"DEBUG: Context now contains: {context.keys()}")
                else:
                    messages.error(request, result.get('error', 'Prediction failed'))
                    print(f"DEBUG: Prediction failed with error: {result.get('error')}")
                
                # Keep form data for display
                context['growth_form_data'] = input_data
                
            except (ValueError, TypeError) as e:
                messages.error(request, f'Invalid input: Please enter valid numbers. {str(e)}')
                # Preserve form data for re-display
                context['growth_form_data'] = {
                    'workers': request.POST.get('workers', ''),
                    'previous_workers': request.POST.get('previous_workers', ''),
                    'revenue': request.POST.get('revenue', ''),
                    'delta_workers': request.POST.get('delta_workers', ''),
                    'founded': request.POST.get('founded', ''),
                    'industry': request.POST.get('industry', ''),
                }
        
        elif prediction_type == 'xgboost_growth':
            # Handle XGBoost company growth prediction
            xgboost_form = XGBoostGrowthPredictionForm(request.POST)
            
            if xgboost_form.is_valid():
                # Extract form data
                input_data = {
                    'years_on_list': xgboost_form.cleaned_data['years_on_list'],
                    'company_age': xgboost_form.cleaned_data['company_age'],
                    'hiring_growth': xgboost_form.cleaned_data['hiring_growth'],
                    'industry': xgboost_form.cleaned_data['industry'],
                    'state': xgboost_form.cleaned_data['state'],
                }
                
                # Import and use the XGBoost growth predictor
                from ml_models.predictors.xgboost_growth_predictor import xgboost_growth_predictor
                
                # Make prediction
                result = xgboost_growth_predictor.predict(input_data)
                
                if result.get('success'):
                    context['xgboost_growth_result'] = result
                    messages.success(request, f"Prediction: {result['growth_category']}")
                    print(f"DEBUG: XGBoost prediction successful! Result: {result}")
                else:
                    messages.error(request, result.get('error', 'Prediction failed'))
                    print(f"DEBUG: XGBoost prediction failed with error: {result.get('error')}")
                
                # Keep form data for display
                context['xgboost_growth_form'] = xgboost_form
            else:
                messages.error(request, 'Please correct the errors in the form')
                context['xgboost_growth_form'] = xgboost_form
    
    print(f"DEBUG: Final context keys before render: {context.keys()}")
    if 'growth_result' in context:
        print(f"DEBUG: growth_result value: {context['growth_result']}")
    if 'growth_form_data' in context:
        print(f"DEBUG: growth_form_data value: {context['growth_form_data']}")
    
    return render(request, 'predictions/employersPredictions.html', context)


def employer_growth_view(request):
    """
    Dedicated view for company growth prediction ONLY
    Employers only - uses growth_lgbm_pipeline(jojo).pkl
    """
    context = {}
    
    if request.method == 'POST':
        # Get form data and convert to proper types
        try:
            workers_input = request.POST.get('workers', '').strip()
            prev_workers_input = request.POST.get('previous_workers', '').strip()
            revenue_input = request.POST.get('revenue', '').strip()
            delta_workers_input = request.POST.get('delta_workers', '').strip()
            founded_input = request.POST.get('founded', '').strip()
            industry_input = request.POST.get('industry', '').strip()
            
            # Validate required fields are not empty
            if not all([workers_input, prev_workers_input, revenue_input, delta_workers_input, founded_input]):
                messages.error(request, 'All required fields must be filled')
                return render(request, 'predictions/employer_growth.html', context)
            
            input_data = {
                'workers': float(workers_input),
                'previous_workers': float(prev_workers_input),
                'revenue': float(revenue_input),
                'delta_workers': float(delta_workers_input),
                'founded': int(founded_input),
                'industry': industry_input if industry_input else 'Other',
            }
        except (ValueError, TypeError) as e:
            messages.error(request, f'Invalid input: Please enter valid numbers. {str(e)}')
            return render(request, 'predictions/employer_growth.html', context)
        
        # Import and use the company growth predictor
        from ml_models.predictors.company_growth_predictor import company_growth_predictor
        
        # Make prediction
        result = company_growth_predictor.predict(input_data)
        
        # Add result to context
        if result.get('success'):
            context['result'] = result
            messages.success(request, f"Predicted Growth: {result['growth_percentage_formatted']}")
        else:
            messages.error(request, result.get('error', 'Prediction failed'))
        
        # Keep form data for display
        context['form_data'] = input_data
    
    return render(request, 'predictions/employer_growth.html', context)

