from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, EmployerProfile, JobSeekerProfile


class CustomLoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserSignupForm(UserCreationForm):
    """Base signup form for user creation"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


class EmployerProfileForm(forms.ModelForm):
    """Form for employer profile information"""
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_website', 'contact_phone', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'company_website': forms.URLInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class JobSeekerProfileForm(forms.ModelForm):
    """Form for job seeker profile information"""
    class Meta:
        model = JobSeekerProfile
        fields = ['bio', 'skills', 'experience_years', 'education_level', 'resume', 'phone', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g., Python, Django, Machine Learning'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
