"""
Input validation utilities for ML predictions
Validates and sanitizes user inputs before passing to models
"""


class InputValidator:
    """Validate inputs for ML predictions"""
    
    @staticmethod
    def validate_salary_input(data):
        """Validate salary prediction inputs"""
        errors = []
        
        if not data.get('job_title'):
            errors.append("Job title is required")
        
        experience = data.get('experience_years')
        if experience is None or experience < 0:
            errors.append("Experience years must be non-negative")
        elif experience > 50:
            errors.append("Experience years seems unusually high")
        
        if not data.get('education_level'):
            errors.append("Education level is required")
        
        if not data.get('location'):
            errors.append("Location is required")
        
        return errors
    
    @staticmethod
    def validate_job_title_input(data):
        """Validate job title prediction inputs"""
        errors = []
        
        if not data.get('skills'):
            errors.append("Skills are required")
        
        experience = data.get('experience_years')
        if experience is None or experience < 0:
            errors.append("Experience years must be non-negative")
        
        return errors
    
    @staticmethod
    def validate_remote_work_input(data):
        """Validate remote work prediction inputs"""
        errors = []
        
        if not data.get('job_title'):
            errors.append("Job title is required")
        
        if not data.get('industry'):
            errors.append("Industry is required")
        
        if not data.get('company_size'):
            errors.append("Company size is required")
        
        return errors
    
    @staticmethod
    def validate_degree_input(data):
        """Validate degree prediction inputs"""
        errors = []
        
        if not data.get('job_title'):
            errors.append("Job title is required")
        
        if not data.get('industry'):
            errors.append("Industry is required")
        
        experience = data.get('experience_years')
        if experience is None or experience < 0:
            errors.append("Experience years must be non-negative")
        
        return errors
    
    @staticmethod
    def validate_benefits_input(data):
        """Validate benefits prediction inputs"""
        errors = []
        
        if not data.get('job_title'):
            errors.append("Job title is required")
        
        if not data.get('company_size'):
            errors.append("Company size is required")
        
        if not data.get('location'):
            errors.append("Location is required")
        
        return errors
    
    @staticmethod
    def validate_company_growth_input(data):
        """Validate company growth prediction inputs"""
        errors = []
        
        if not data.get('company_name'):
            errors.append("Company name is required")
        
        if not data.get('industry'):
            errors.append("Industry is required")
        
        employee_count = data.get('employee_count')
        if employee_count is None or employee_count < 1:
            errors.append("Employee count must be at least 1")
        
        years = data.get('years_in_business')
        if years is None or years < 0:
            errors.append("Years in business must be non-negative")
        
        return errors
    
    @staticmethod
    def validate_revenue_growth_input(data):
        """Validate revenue growth prediction inputs"""
        errors = []
        
        if not data.get('company_name'):
            errors.append("Company name is required")
        
        revenue = data.get('current_revenue')
        if revenue is None or revenue < 0:
            errors.append("Current revenue must be non-negative")
        
        if not data.get('industry'):
            errors.append("Industry is required")
        
        market_share = data.get('market_share')
        if market_share is None or market_share < 0 or market_share > 100:
            errors.append("Market share must be between 0 and 100")
        
        return errors
    
    @staticmethod
    def validate_campaign_conversion_input(data):
        """Validate campaign conversion prediction inputs"""
        errors = []
        
        if not data.get('campaign_name'):
            errors.append("Campaign name is required")
        
        budget = data.get('budget')
        if budget is None or budget < 0:
            errors.append("Budget must be non-negative")
        
        audience_size = data.get('target_audience_size')
        if audience_size is None or audience_size < 1:
            errors.append("Target audience size must be at least 1")
        
        duration = data.get('duration_days')
        if duration is None or duration < 1:
            errors.append("Campaign duration must be at least 1 day")
        
        return errors


# Global validator instance
validator = InputValidator()
