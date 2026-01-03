from django import forms
from .models import Job, JobApplication


class JobForm(forms.ModelForm):
    """Form for creating and updating job postings"""
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'location', 
            'job_type', 'salary_min', 'salary_max', 'is_remote', 
            'application_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Job Description'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Job Requirements'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min Salary'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Salary'}),
            'is_remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class JobApplicationForm(forms.ModelForm):
    """Form for job seekers to apply for jobs"""
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'Tell the employer why you are a great fit for this position...'
            }),
        }
