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
    """Form for remote work eligibility prediction"""
    
    INDUSTRY_CHOICES = [
        ('', '-- Select Industry --'),
        ('Advertising & Marketing', 'Advertising & Marketing'),
        ('Business Products & Services', 'Business Products & Services'),
        ('Computer Hardware', 'Computer Hardware'),
        ('Construction', 'Construction'),
        ('Consumer Products & Services', 'Consumer Products & Services'),
        ('Education', 'Education'),
        ('Energy', 'Energy'),
        ('Engineering', 'Engineering'),
        ('Environmental Services', 'Environmental Services'),
        ('Financial Services', 'Financial Services'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Government Services', 'Government Services'),
        ('Health', 'Health'),
        ('Human Resources', 'Human Resources'),
        ('Insurance', 'Insurance'),
        ('IT Management', 'IT Management'),
        ('IT Services', 'IT Services'),
        ('IT System Development', 'IT System Development'),
        ('Logistics & Transportation', 'Logistics & Transportation'),
        ('Manufacturing', 'Manufacturing'),
        ('Media', 'Media'),
        ('Real Estate', 'Real Estate'),
        ('Retail', 'Retail'),
        ('Security', 'Security'),
        ('Software', 'Software'),
        ('Telecommunications', 'Telecommunications'),
        ('Travel & Hospitality', 'Travel & Hospitality'),
    ]
    
    job_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}))
    industry = forms.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the industry that matches your training data'
    )
    company_size = forms.ChoiceField(
        choices=[
            ('small', 'Small (1-50)'),
            ('medium', 'Medium (51-500)'),
            ('large', 'Large (500+)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
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
    """Form for marketing campaign conversion prediction"""
    
    COMPANY_CHOICES = [
        ('', 'Select Company'),
        ('Innovate Industries', 'Innovate Industries'),
        ('NexGen Systems', 'NexGen Systems'),
        ('Alpha Innovations', 'Alpha Innovations'),
        ('DataTech Solutions', 'DataTech Solutions'),
        ('TechCorp', 'TechCorp'),
    ]
    
    LOCATION_CHOICES = [
        ('', 'Select Location'),
        ('Chicago', 'Chicago'),
        ('Houston', 'Houston'),
        ('Los Angeles', 'Los Angeles'),
        ('Miami', 'Miami'),
        ('New York', 'New York'),
    ]
    
    CAMPAIGN_TYPE_CHOICES = [
        ('', 'Select Campaign Type'),
        ('Email', 'Email'),
        ('Influencer', 'Influencer'),
        ('Search', 'Search'),
        ('Social Media', 'Social Media'),
    ]
    
    TARGET_AUDIENCE_CHOICES = [
        ('', 'Select Target Audience'),
        ('All Ages', 'All Ages'),
        ('Men 18-24', 'Men 18-24'),
        ('Men 25-34', 'Men 25-34'),
        ('Women 25-34', 'Women 25-34'),
        ('Women 35-44', 'Women 35-44'),
    ]
    
    CHANNEL_CHOICES = [
        ('', 'Select Channel'),
        ('Email', 'Email'),
        ('Facebook', 'Facebook'),
        ('Google Ads', 'Google Ads'),
        ('Instagram', 'Instagram'),
        ('Website', 'Website'),
        ('YouTube', 'YouTube'),
    ]
    
    LANGUAGE_CHOICES = [
        ('', 'Select Language'),
        ('English', 'English'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
        ('Mandarin', 'Mandarin'),
        ('German', 'German'),
    ]
    
    CUSTOMER_SEGMENT_CHOICES = [
        ('', 'Select Customer Segment'),
        ('Fashionistas', 'Fashionistas'),
        ('Health & Wellness', 'Health & Wellness'),
        ('Outdoor Adventurers', 'Outdoor Adventurers'),
        ('Foodies', 'Foodies'),
        ('Tech Enthusiasts', 'Tech Enthusiasts'),
    ]
    
    company = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'})
    )
    
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})
    )
    
    campaign_type = forms.ChoiceField(
        choices=CAMPAIGN_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    target_audience = forms.ChoiceField(
        choices=TARGET_AUDIENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    duration = forms.IntegerField(
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Campaign duration in days'
        }),
        help_text='Duration in days (1-365)'
    )
    
    channel_used = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    customer_segment = forms.ChoiceField(
        choices=CUSTOMER_SEGMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    """Form for campaign conversion prediction"""
    campaign_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Name'}))
    budget = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign budget'}))
    target_audience_size = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target audience size'}))
    duration_days = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign duration (days)'}))


class XGBoostGrowthPredictionForm(forms.Form):
    """Form for XGBoost company growth prediction"""
    years_on_list = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 5'
        }),
        help_text='Number of years the company has been on the list'
    )
    company_age = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 15'
        }),
        help_text='Age of the company in years'
    )
    hiring_growth = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 12.5',
            'step': '0.01'
        }),
        help_text='Hiring growth rate as percentage'
    )
    industry = forms.ChoiceField(
        choices=[],  # Will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the company industry'
    )
    state = forms.ChoiceField(
        choices=[],  # Will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the US state where company is located'
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize form and populate dynamic choices"""
        super().__init__(*args, **kwargs)
        # Import here to avoid circular import
        from ml_models.predictors.xgboost_growth_predictor import xgboost_growth_predictor
        
        # Populate industry choices
        industry_choices = xgboost_growth_predictor.get_industry_choices()
        if industry_choices:
            self.fields['industry'].choices = [('', '-- Select Industry --')] + industry_choices
        
        # Populate state choices
        state_choices = xgboost_growth_predictor.get_state_choices()
        if state_choices:
            self.fields['state'].choices = [('', '-- Select State --')] + state_choices
