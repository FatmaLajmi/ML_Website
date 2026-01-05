"""
ML Models Predictors Package
Import all predictors for easy access
"""
from .salary_predictor import salary_predictor
from .job_title_predictor import job_title_predictor
from .remote_work_predictor import remote_work_predictor
from .degree_predictor import degree_predictor
from .benefits_predictor import benefits_predictor
from .company_growth_predictor import company_growth_predictor
from .revenue_growth_predictor import revenue_growth_predictor
from .campaign_conversion_predictor import campaign_conversion_predictor

__all__ = [
    'salary_predictor',
    'job_title_predictor',
    'remote_work_predictor',
    'degree_predictor',
    'benefits_predictor',
    'company_growth_predictor',
    'revenue_growth_predictor',
    'campaign_conversion_predictor',
]
