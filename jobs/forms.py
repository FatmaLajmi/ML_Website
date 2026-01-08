from django import forms
from .models import Job, JobApplication


class JobForm(forms.ModelForm):
    """Form for employers to post jobs"""
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'company_description', 'company_website',
                  'location', 'salary_range', 
                  'job_type', 'experience_level', 'education_level', 'skills_required',
                  'degree_required', 'remote_option', 'benefits', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior Software Engineer'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detailed job description, responsibilities, and company culture...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'List job requirements and qualifications...'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of your company...'}),
            'company_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.yourcompany.com'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., New York, NY or Remote'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., $50,000 - $70,000 (optional)'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'skills_required': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Python, Django, JavaScript, SQL (comma-separated)'}),
            'degree_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remote_option': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'e.g., Health insurance, 401(k), Flexible hours (optional)'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Job Title *',
            'description': 'Job Description *',
            'requirements': 'Requirements',
            'company_description': 'Company Description',
            'company_website': 'Company Website',
            'location': 'Location *',
            'salary_range': 'Salary Range',
            'job_type': 'Job Type *',
            'experience_level': 'Experience Level',
            'education_level': 'Education Level',
            'skills_required': 'Skills Required',
            'degree_required': 'Degree Required',
            'remote_option': 'Remote Work Available',
            'benefits': 'Benefits',
            'deadline': 'Application Deadline',
        }


class JobApplicationForm(forms.ModelForm):
    """Minimal form for job applications"""
    class Meta:
        model = JobApplication
        fields = []
        # Job and applicant are set in the view
