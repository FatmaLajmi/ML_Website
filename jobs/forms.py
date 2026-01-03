from django import forms
from .models import Job, JobApplication


class JobForm(forms.ModelForm):
    """Form for employers to post jobs"""
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary_range', 'job_type', 
                  'degree_required', 'remote_option', 'benefits']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Job Description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., $50,000 - $70,000 (optional)'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'degree_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remote_option': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Benefits (optional)'}),
        }
        labels = {
            'title': 'Job Title *',
            'description': 'Job Description *',
            'location': 'Location *',
            'salary_range': 'Salary Range',
            'job_type': 'Job Type *',
            'degree_required': 'Degree Required',
            'remote_option': 'Remote Work Available',
            'benefits': 'Benefits',
        }


class JobApplicationForm(forms.ModelForm):
    """Minimal form for job applications"""
    class Meta:
        model = JobApplication
        fields = []
        # Job and applicant are set in the view
