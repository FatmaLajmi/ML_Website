"""
Salary Prediction Module (Regression)
Predicts salary based on job characteristics using log-salary regression
Authors: Zeineb & Eya

FEATURES: Complete feature engineering pipeline (170+ columns)
- 90+ one-hot encoded skills
- 6 seniority features
- 6 technology category features
- 3 temporal features
- 15+ basic job features
- 3 company features
- 2 interaction features
"""
import pandas as pd
import numpy as np
from pathlib import Path
import traceback
from datetime import datetime

try:
    import joblib
except Exception:
    joblib = None

try:
    import pickle
except Exception:
    pickle = None

# ============================================================================
# COMPLETE FEATURE ENGINEERING PIPELINE (170+ COLUMNS)
# ============================================================================

# Define all available skills for one-hot encoding (from model training)
AVAILABLE_SKILLS = [
    'python', 'java', 'sql', 'javascript', 'c', 'cpp', 'csharp', 'go', 'golang',
    'rust', 'swift', 'kotlin', 'scala', 'ruby', 'perl', 'php', 'r', 'matlab',
    'julia', 'assembly', 'visual_basic', 'crystal', 'node', 'node.js', 'react',
    'angular', 'django', 'flask', 'fastapi', 'spring', 'express', 'hadoop',
    'spark', 'pyspark', 'kafka', 'airflow', 'databricks', 'snowflake',
    'bigquery', 'redshift', 'postgresql', 'mysql', 'oracle', 'mongodb', 'mongo',
    'cassandra', 'dynamodb', 'redis', 'elasticsearch', 'neo4j', 'db2',
    'sql_server', 't-sql', 'no-sql', 'nosql', 'aurora', 'aws', 'azure', 'gcp', 
    'ibm_cloud', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 
    'numpy', 'matplotlib', 'seaborn', 'plotly', 'ggplot2', 'tidyverse', 'rshiny', 
    'jupyter', 'git', 'github', 'gitlab', 'bitbucket', 'svn', 'docker', 
    'kubernetes', 'terraform', 'ansible', 'jenkins', 'linux', 'unix', 'windows', 
    'bash', 'shell', 'powershell', 'terminal', 'jira', 'confluence', 'slack', 
    'zoom', 'excel', 'powerpoint', 'word', 'ms_access', 'outlook', 'google_sheets',
    'tableau', 'power_bi', 'looker', 'qlik', 'microstrategy', 'cognos',
    'alteryx', 'datarobot', 'sas', 'spss', 'visio', 'smartsheet',
    'planner', 'notion', 'flow', 'hugging_face', 'opencv', 'nltk', 'mxnet',
    'theano', 'vba', 'spreadsheet', 'gdpr', 'sap', 'unify', 'ssrs',
    'ssis', 'dax', 'chef', 'yarn', 'phoenix', 'unity',
    'html', 'css', 'jquery', 'typescript', 'graphql', 'selenium', 'splunk',
    'atlassian', 'watson', 'sharepoint'
]


def extract_skills_from_text(skills_text):
    """Extract individual skills and create one-hot encoding"""
    if not skills_text:
        return {}
    
    # Parse and normalize skills
    skills_list = [s.strip().lower().replace(' ', '_').replace('-', '_') 
                   for s in skills_text.split(',') if s.strip()]
    
    # Create one-hot encoding for ALL skills
    skill_features = {}
    for skill in AVAILABLE_SKILLS:
        skill_col = f'skill_{skill}'
        # Check if this skill matches any user skill
        skill_features[skill_col] = 1 if any(skill in s for s in skills_list) else 0
    
    return skill_features


def classify_seniority(job_title):
    """Classify job title into seniority levels"""
    title_lower = (job_title or '').lower()
    
    senior_keywords = ['senior', 'sr.', 'sr ', 'lead', 'principal', 'architect']
    manager_keywords = ['manager', 'director', 'vp', 'head', 'chief']
    principal_keywords = ['principal', 'distinguished', 'fellow']
    junior_keywords = ['junior', 'jr.', 'jr ', 'entry', 'entry-level', 'graduate']
    
    is_senior = 1 if any(kw in title_lower for kw in senior_keywords) else 0
    is_manager = 1 if any(kw in title_lower for kw in manager_keywords) else 0
    is_principal = 1 if any(kw in title_lower for kw in principal_keywords) else 0
    is_lead = 1 if 'lead' in title_lower else 0
    is_junior = 1 if any(kw in title_lower for kw in junior_keywords) else 0
    
    # Determine experience level (0-4)
    if is_principal:
        exp_level = 4
    elif is_manager or is_lead:
        exp_level = 3
    elif is_senior:
        exp_level = 2
    elif is_junior:
        exp_level = 0
    else:
        exp_level = 1  # Mid-level default
    
    return {
        'is_senior': is_senior,
        'is_manager': is_manager,
        'is_principal': is_principal,
        'is_lead': is_lead,
        'is_junior': is_junior,
        'exp_level': exp_level,
    }


def create_technology_features(skills_text):
    """Categorize skills into technology groups"""
    skills_lower = (skills_text or '').lower()
    
    big_data_keywords = ['hadoop', 'spark', 'kafka', 'airflow', 'databricks', 'hive']
    ml_keywords = ['tensorflow', 'pytorch', 'keras', 'scikit', 'sklearn', 'xgboost']
    db_keywords = ['sql', 'postgres', 'mysql', 'oracle', 'mongodb', 'cassandra', 'redis']
    programming_keywords = ['python', 'java', 'scala', 'r', 'go', 'rust', 'javascript']
    bi_keywords = ['tableau', 'power_bi', 'looker', 'qlik', 'cognos', 'microstrategy']
    cloud_keywords = ['aws', 'azure', 'gcp', 'cloud']
    
    return {
        'has_bigdata': 1 if any(kw in skills_lower for kw in big_data_keywords) else 0,
        'has_ml_lib': 1 if any(kw in skills_lower for kw in ml_keywords) else 0,
        'has_db': 1 if any(kw in skills_lower for kw in db_keywords) else 0,
        'has_programming': 1 if any(kw in skills_lower for kw in programming_keywords) else 0,
        'has_bi_tool': 1 if any(kw in skills_lower for kw in bi_keywords) else 0,
        'has_cloud': 1 if any(kw in skills_lower for kw in cloud_keywords) else 0,
    }


def prepare_complete_features(input_data):
    """
    MAIN: Convert minimal user input to 170+ required features
    """
    # Extract and normalize inputs
    job_title = (input_data.get('job_title_short', '') or '').lower().strip()
    job_country = (input_data.get('job_country', '') or 'us').lower().strip()
    job_state = (input_data.get('job_state', '') or 'unknown').lower().strip()
    skills_text = (input_data.get('skills_text', '') or '').lower().strip()
    job_schedule = (input_data.get('job_schedule_type', '') or 'full_time').lower().strip()
    remote_option = input_data.get('remote_option', 0)
    
    # Initialize feature dictionary
    all_features = {}
    
    # ==================== Basic Features ====================
    all_features['job_title_short'] = job_title
    all_features['job_title_short_len'] = len(job_title)
    all_features['job_title_len'] = len(job_title)
    all_features['us_state'] = job_state
    all_features['job_country'] = job_country  # Add this as a feature column
    all_features['job_schedule_type'] = job_schedule
    all_features['job_via'] = 'linkedin'
    all_features['job_work_from_home'] = remote_option
    all_features['job_no_degree_mention'] = 0
    all_features['job_health_insurance'] = 1
    
    # ==================== Skill Features (One-Hot) ====================
    skill_features = extract_skills_from_text(skills_text)
    all_features.update(skill_features)
    
    # ==================== Temporal Features ====================
    now = datetime.now()
    all_features['posted_month'] = now.month
    all_features['posted_year'] = now.year
    all_features['posted_dayofweek'] = now.weekday()
    
    # ==================== Seniority Features ====================
    seniority_features = classify_seniority(job_title)
    all_features.update(seniority_features)
    
    # ==================== Technology Category Features ====================
    tech_features = create_technology_features(skills_text)
    all_features.update(tech_features)
    
    # ==================== Skill Statistics ====================
    skills_list = [s.strip() for s in skills_text.split(',') if s.strip()]
    all_features['n_skills'] = len(skills_list)
    all_features['n_skill_groups'] = len([v for v in tech_features.values() if v == 1])
    all_features['skill_value_mean'] = 0.5
    
    # ==================== Company Features ====================
    all_features['company_name_reduced'] = 'other'
    all_features['company_posting_log'] = np.log(10)
    all_features['role_family'] = 'data'
    
    # ==================== Interaction Features ====================
    all_features['remote_x_senior'] = remote_option * all_features['is_senior']
    is_ds = 1 if 'scientist' in job_title or 'analyst' in job_title else 0
    all_features['cloud_x_ds'] = all_features['has_cloud'] * is_ds
    
    # ==================== Convert to DataFrame ====================
    df = pd.DataFrame([all_features])
    
    return df, all_features


def _get_model():
    """Load the salary regression model"""
    model_path = Path(__file__).parent.parent / "models" / "salary_regression_model(zeineb+eya).pkl"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Try joblib first (preferred for sklearn models)
    if joblib is not None:
        try:
            return joblib.load(model_path)
        except Exception as e:
            print(f"joblib.load failed: {e}")
    
    # Fallback to pickle
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"pickle.load failed: {e}")
        raise FileNotFoundError(f"Could not load model: {model_path}")


def validate_salary_input(data):
    """Validate salary prediction input"""
    errors = []
    
    if not data.get('job_title_short', '').strip():
        errors.append("Job title is required")
    
    if not data.get('job_country', '').strip():
        errors.append("Country is required")
    
    if not data.get('skills_text', '').strip():
        errors.append("Skills are required")
    
    return errors


def calculate_num_skills(skills_text):
    """
    Calculate number of skills from comma-separated text
    Option 1: Split by comma and count non-empty items
    """
    if not skills_text or not skills_text.strip():
        return 0
    
    skills = [s.strip() for s in skills_text.split(',') if s.strip()]
    return len(skills)


def calculate_title_length(job_title_short):
    """Calculate character length of job title"""
    return len(job_title_short.strip()) if job_title_short else 0


def predict_salary(data: dict) -> dict:
    """
    Predict salary using regression model
    
    Uses COMPLETE FEATURE ENGINEERING to generate 170+ required columns
    
    Args:
        data: Dictionary with keys:
            - job_title_short (required): Job title
            - job_country (required): Country
            - job_state (optional): State/Region
            - skills_text (required): Comma-separated skills
            - job_schedule_type (optional): full_time/part_time
            - remote_option (optional): 0 or 1
    
    Returns:
        Dictionary with prediction results including estimated salary
    """
    try:
        # Validate input
        errors = validate_salary_input(data)
        if errors:
            return {'success': False, 'error': ', '.join(errors)}
        
        # Load model
        model = _get_model()
        
        # ===== COMPLETE FEATURE ENGINEERING (170+ columns) =====
        X, features_dict = prepare_complete_features(data)
        
        print(f"✅ Generated {len(features_dict)} features for model")
        print(f"   Skill columns: {sum(1 for k in features_dict if k.startswith('skill_'))}")
        print(f"   DataFrame shape: {X.shape}")
        
        # Make prediction (model predicts log-salary)
        log_salary_pred = float(model.predict(X)[0])
        
        # Convert log-salary back to actual salary
        salary_pred = float(np.exp(log_salary_pred))
        salary_pred = round(salary_pred, 0)
        
        # Safety bounds: $20k to $500k
        if salary_pred < 20000:
            salary_pred = 20000
        elif salary_pred > 500000:
            salary_pred = 500000
        
        num_skills = features_dict.get('n_skills', 0)
        
        return {
            'success': True,
            'prediction': f"${salary_pred:,.0f}",
            'salary_value': salary_pred,
            'log_salary': round(log_salary_pred, 4),
            'currency': 'USD',
            'job_title': data.get('job_title_short', ''),
            'num_skills': num_skills,
            'features_count': len(features_dict),
        }
    
    except FileNotFoundError as e:
        return {'success': False, 'error': f'Model file not found: {str(e)}'}
    except ValueError as e:
        return {'success': False, 'error': f'Invalid input: {str(e)}'}
    except Exception as e:
        print(f"Salary prediction error: {traceback.format_exc()}")
        return {'success': False, 'error': f'Prediction failed: {str(e)}'}


class SalaryPredictor:
    """Salary prediction handler - compatible interface"""
    
    def predict(self, data: dict) -> dict:
        """Make prediction using predict_salary function"""
        return predict_salary(data)


# Global predictor instance for consistency with other predictors
salary_predictor = SalaryPredictor()
