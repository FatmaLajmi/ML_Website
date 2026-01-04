from django.shortcuts import render
from django.contrib import messages
from .forms import (
    SalaryPredictionForm, JobTitlePredictionForm, RemoteWorkPredictionForm,
    DegreePredictionForm, BenefitsPredictionForm, CompanyGrowthPredictionForm,
    RevenueGrowthPredictionForm, CampaignConversionPredictionForm
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
    }
    
    # TODO: Implement employer predictions handling
    
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

