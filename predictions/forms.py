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


SCHEDULE_CHOICES = [
    ("full-time", "Full-time"),
    ("part-time", "Part-time"),
    ("contract", "Contract"),
    ("internship", "Internship"),
]

YES_NO = [
    ("Yes", "Yes"),
    ("No", "No"),
]

COUNTRY_CHOICES = [
    ("USA", "USA"),
    ("UK", "UK"),
    ("Canada", "Canada"),
    ("France", "France"),
    ("Germany", "Germany"),
    ("Other", "Other"),
]

COMPANY_SIZE_CHOICES = [
    ("Small", "Small"),
    ("Medium", "Medium"),
    ("Large", "Large"),
]

class HealthInsuranceForm(forms.Form):
    job_title_short = forms.CharField(
        label="Job title",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Data Scientist"}),
    )
    job_schedule_type = forms.ChoiceField(
        label="Schedule type",
        choices=SCHEDULE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    job_work_from_home = forms.ChoiceField(
        label="Remote work?",
        choices=YES_NO,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    job_country = forms.ChoiceField(
        label="Country",
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    company_name = forms.CharField(
        label="Company name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Google"}),
    )

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

class SalaryPredictionForm(forms.Form):
    """Form for salary prediction using regression model"""
    
    COUNTRY_CHOICES = [
        ('', '-- Select Country --'),
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IN', 'India'),
        ('SG', 'Singapore'),
        ('NL', 'Netherlands'),
    ]
    
    STATE_CHOICES = [
        ('', '-- Select State --'),
        ('CA', 'California'),
        ('NY', 'New York'),
        ('TX', 'Texas'),
        ('FL', 'Florida'),
        ('WA', 'Washington'),
        ('MA', 'Massachusetts'),
        ('IL', 'Illinois'),
        ('PA', 'Pennsylvania'),
        ('CO', 'Colorado'),
        ('Unknown', 'Other/Unknown'),
    ]
    
    job_title_short = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., data scientist, backend engineer, product manager'
        }),
        label='Job Title',
        help_text='Enter the job title (short form)'
    )
    
    job_country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Country'
    )
    
    job_state = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='State/Region',
        required=False
    )
    
    skills_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'e.g., python, sql, machine learning, aws, docker'
        }),
        label='Skills (comma-separated)',
        help_text='List main skills required for the job'
    )