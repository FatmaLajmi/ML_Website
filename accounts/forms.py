from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, EmployerProfile, JobSeekerProfile, Skill


class CustomLoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class SignupForm(UserCreationForm):
    """Unified signup form with conditional fields based on role"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES[:2],  # Only employer and job_seeker
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'role-select'})
    )
    
    # Employer fields
    company_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control employer-field', 'placeholder': 'Company Name'})
    )
    industry = forms.ChoiceField(
        choices=EmployerProfile.INDUSTRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control employer-field'})
    )
    company_size = forms.ChoiceField(
        choices=EmployerProfile.COMPANY_SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control employer-field'})
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control employer-field', 'placeholder': 'Company Website (optional)'})
    )
    
    # Job Seeker fields
    education_level = forms.ChoiceField(
        choices=JobSeekerProfile.EDUCATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control jobseeker-field'})
    )
    years_experience = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control jobseeker-field', 'placeholder': 'Years of Experience'})
    )
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'skill-checkbox jobseeker-field'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        # Validate employer fields
        if role == 'employer':
            if not cleaned_data.get('company_name'):
                self.add_error('company_name', 'This field is required for employers.')
            if not cleaned_data.get('industry'):
                self.add_error('industry', 'This field is required for employers.')
            if not cleaned_data.get('company_size'):
                self.add_error('company_size', 'This field is required for employers.')
        
        # Validate job seeker fields
        if role == 'job_seeker':
            if not cleaned_data.get('education_level'):
                self.add_error('education_level', 'This field is required for job seekers.')
            if cleaned_data.get('years_experience') is None:
                self.add_error('years_experience', 'This field is required for job seekers.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        
        if commit:
            user.save()
            
            # Create profile based on role
            if user.role == 'employer':
                EmployerProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'company_name': self.cleaned_data['company_name'],
                        'industry': self.cleaned_data['industry'],
                        'company_size': self.cleaned_data['company_size'],
                        'website': self.cleaned_data.get('website', ''),
                    }
                )
            elif user.role == 'job_seeker':
                profile, created = JobSeekerProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'education_level': self.cleaned_data['education_level'],
                        'years_experience': self.cleaned_data['years_experience'],
                    }
                )
                # Add skills
                skills = self.cleaned_data.get('skills', [])
                profile.skills.set(skills)
        
        return user


class EmployerProfileForm(forms.ModelForm):
    """Form for editing employer profile"""
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'industry', 'company_size', 'website', 'company_description', 'location', 'contact_phone']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.Select(attrs={'class': 'form-control'}),
            'company_size': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class JobSeekerProfileForm(forms.ModelForm):
    """Form for editing job seeker profile"""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'skill-checkbox'})
    )
    
    class Meta:
        model = JobSeekerProfile
        fields = ['education_level', 'years_experience', 'skills', 'bio', 'resume', 'phone', 'location']
        widgets = {
            'education_level': forms.Select(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
