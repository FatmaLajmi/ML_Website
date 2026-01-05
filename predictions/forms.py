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
    """Form for campaign conversion prediction"""
    campaign_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Name'}))
    budget = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign budget'}))
    target_audience_size = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target audience size'}))
    duration_days = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Campaign duration (days)'}))

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
