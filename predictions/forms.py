from django import forms


class SalaryPredictionForm(forms.Form):
    """Form for salary prediction input"""
    job_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Engineer'}))
    experience_years = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}))
    education_level = forms.ChoiceField(
        choices=[
            ('high_school', 'High School'),
            ('bachelors', 'Bachelors'),
            ('masters', 'Masters'),
            ('phd', 'PhD'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City or Country'}))


class JobTitlePredictionForm(forms.Form):
    """Form for job title prediction based on skills"""
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your skills (comma-separated)'}),
        help_text='e.g., Python, Django, Machine Learning, SQL'
    )
    experience_years = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}))


class RemoteWorkPredictionForm(forms.Form):
    """Form for remote work prediction - with validated choices from trained model"""
    
    # These choices match the model's training data exactly
    JOB_TITLES = [
        ('Business Analyst', 'Business Analyst'),
        ('Cloud Engineer', 'Cloud Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('Data Engineer', 'Data Engineer'),
        ('Data Scientist', 'Data Scientist'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),
        ('Senior Data Analyst', 'Senior Data Analyst'),
        ('Senior Data Engineer', 'Senior Data Engineer'),
        ('Senior Data Scientist', 'Senior Data Scientist'),
        ('Software Engineer', 'Software Engineer'),
    ]
    
    SENIORITY_LEVELS = [
        ('Lead', 'Lead'),
        ('Mid', 'Mid-Level'),
        ('Senior', 'Senior'),
    ]
    
    COUNTRIES = [
        ('United States', 'United States'),
        ('Canada', 'Canada'),
        ('United Kingdom', 'United Kingdom'),
        ('France', 'France'),
        ('Germany', 'Germany'),
        ('Australia', 'Australia'),
        ('India', 'India'),
        ('China', 'China'),
        ('Japan', 'Japan'),
        ('Brazil', 'Brazil'),
        ('Mexico', 'Mexico'),
        ('Netherlands', 'Netherlands'),
        ('Spain', 'Spain'),
        ('Italy', 'Italy'),
        ('Singapore', 'Singapore'),
        ('Hong Kong', 'Hong Kong'),
        ('Ireland', 'Ireland'),
    ]
    
    SCHEDULE_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contractor', 'Contractor'),
        ('Internship', 'Internship'),
        ('Temp work', 'Temp work'),
        ('Unknown', 'Unknown'),
    ]
    
    job_title_short = forms.ChoiceField(
        choices=JOB_TITLES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Job Title"
    )

    job_seniority = forms.ChoiceField(
        choices=SENIORITY_LEVELS,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Seniority Level"
    )

    job_country = forms.ChoiceField(
        choices=COUNTRIES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Country"
    )

    job_schedule_type = forms.ChoiceField(
        choices=SCHEDULE_TYPES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Schedule Type"
    )

    text_block = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Paste job description / skills / tools ..."}),
        label="Job Description"
    )


class DegreePredictionForm(forms.Form):
    """Form for degree requirement prediction using XGBoost model"""
    skill_count = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of skills required (e.g., 5)'
        }),
        help_text='Total number of skills mentioned in the job posting'
    )
    job_title_short = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Software Engineer, Data Analyst'
        }),
        help_text='Simplified job title'
    )
    job_via = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., LinkedIn, Indeed, Company Website'
        }),
        help_text='Platform where the job was posted'
    )
    company_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Google, Microsoft, Startup Inc.'
        }),
        help_text='Name of the hiring company'
    )
    job_country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., United States, Canada, UK'
        }),
        help_text='Country where the job is located'
    )
    search_location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., New York, San Francisco, Remote'
        }),
        help_text='Specific location or city for the job'
    )


class BenefitsPredictionForm(forms.Form):
    """Form for benefits prediction"""
    job_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}))
    company_size = forms.ChoiceField(
        choices=[
            ('small', 'Small (1-50)'),
            ('medium', 'Medium (51-500)'),
            ('large', 'Large (500+)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}))


class CompanyGrowthPredictionForm(forms.Form):
    """Form for company growth prediction"""
    company_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
    industry = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}))
    employee_count = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of employees'}))
    years_in_business = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years in business'}))


class RevenueGrowthPredictionForm(forms.Form):
    """Form for revenue growth prediction"""
    company_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}))
    current_revenue = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Current annual revenue'}))
    industry = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}))
    market_share = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Market share (%)'}))


class CampaignConversionPredictionForm(forms.Form):
    """Form for campaign conversion prediction"""
    campaign_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Name'}))
    budget = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign budget'}))
    target_audience_size = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target audience size'}))
    duration_days = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign duration (days)'}))
