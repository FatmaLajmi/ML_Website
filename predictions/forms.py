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
    job_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}))
    industry = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}))
    company_size = forms.ChoiceField(
        choices=[
            ('small', 'Small (1-50)'),
            ('medium', 'Medium (51-500)'),
            ('large', 'Large (500+)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DegreePredictionForm(forms.Form):
    """Form for required degree prediction"""
    job_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}))
    industry = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Industry'}))
    experience_years = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}))


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
    
    company = forms.ChoiceField(
        choices=COMPANY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
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
