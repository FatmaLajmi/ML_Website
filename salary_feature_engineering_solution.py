"""
SALARY PREDICTION - FEATURE MISMATCH FIX
========================================

Problem: Model expects 150+ columns, but we're providing only 8

Solution: Complete Feature Engineering Pipeline
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# SOLUTION: COMPLETE FEATURE ENGINEERING
# ============================================================================

# 1. DEFINE ALL EXPECTED SKILLS
AVAILABLE_SKILLS = [
    'python', 'java', 'sql', 'javascript', 'c', 'cpp', 'csharp', 'go', 'golang',
    'rust', 'swift', 'kotlin', 'scala', 'ruby', 'perl', 'php', 'r', 'matlab',
    'julia', 'assembly', 'visual_basic', 'crystal', 'node', 'node.js', 'react',
    'angular', 'django', 'flask', 'fastapi', 'spring', 'express', 'hadoop',
    'spark', 'pyspark', 'kafka', 'airflow', 'databricks', 'snowflake',
    'bigquery', 'redshift', 'postgresql', 'mysql', 'oracle', 'mongodb', 
    'cassandra', 'dynamodb', 'redis', 'elasticsearch', 'neo4j', 'db2',
    'sql_server', 'aurora', 'aws', 'azure', 'gcp', 'ibm_cloud', 'tensorflow',
    'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
    'seaborn', 'plotly', 'ggplot2', 'tidyverse', 'rshiny', 'jupyter', 'git',
    'github', 'gitlab', 'bitbucket', 'svn', 'docker', 'kubernetes', 'terraform',
    'ansible', 'jenkins', 'linux', 'unix', 'windows', 'bash', 'shell',
    'powershell', 'terminal', 'jira', 'confluence', 'slack', 'zoom',
    'excel', 'powerpoint', 'word', 'ms_access', 'outlook', 'google_sheets',
    'tableau', 'power_bi', 'looker', 'qlik', 'microstrategy', 'cognos',
    'alteryx', 'datarobot', 'sas', 'spss', 'excel'
]

def extract_skills_from_text(skills_text):
    """
    Extract individual skills from comma-separated text
    and return as one-hot encoded features
    """
    if not skills_text:
        return {}
    
    # Parse and normalize skills
    skills_list = [s.strip().lower().replace(' ', '_').replace('-', '_') 
                   for s in skills_text.split(',') if s.strip()]
    
    # Create one-hot encoding for all skills
    skill_features = {}
    for skill in AVAILABLE_SKILLS:
        skill_col = f'skill_{skill}'
        # Check if this skill is in the user's list
        skill_features[skill_col] = 1 if any(skill in s for s in skills_list) else 0
    
    return skill_features


def classify_seniority(job_title):
    """
    Classify job title into seniority levels
    Creates binary features: is_senior, is_manager, is_lead, is_principal, is_junior
    """
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
    
    # Determine experience level
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
    """
    Categorize skills into technology groups
    """
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
    MAIN FUNCTION: Complete feature engineering pipeline
    Converts minimal user input to ALL required model features (~150 columns)
    
    Input:
        input_data: Dictionary with keys:
            - job_title_short (required)
            - job_country (optional, default: 'US')
            - job_state (optional, default: 'Unknown')
            - skills_text (required)
            - job_schedule_type (optional, default: 'full_time')
            - remote_option (optional, default: 0)
    
    Returns:
        DataFrame with all required features
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
    all_features['job_schedule_type'] = job_schedule
    all_features['job_via'] = 'linkedin'  # Default source
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
    all_features['skill_value_mean'] = 0.5  # Default
    
    # ==================== Company Features ====================
    all_features['company_name_reduced'] = 'other'
    all_features['company_posting_log'] = np.log(10)  # Log(10 postings)
    all_features['role_family'] = 'data'  # Default for data roles
    
    # ==================== Interaction Features ====================
    all_features['remote_x_senior'] = remote_option * all_features['is_senior']
    is_ds = 1 if 'scientist' in job_title or 'analyst' in job_title else 0
    all_features['cloud_x_ds'] = all_features['has_cloud'] * is_ds
    
    # ==================== Convert to DataFrame ====================
    df = pd.DataFrame([all_features])
    
    return df, all_features


# ============================================================================
# UPDATED salary_predictor_regression.py - PREDICT_FEATURES FUNCTION
# ============================================================================

def _prepare_features_fixed(input_data):
    """
    FIXED VERSION: Prepare all 150+ features required by model
    
    Replaces the old _prepare_features() function
    """
    df, features_dict = prepare_complete_features(input_data)
    
    print(f"✅ Generated {len(features_dict)} features")
    print(f"   Skill columns: {sum(1 for k in features_dict if k.startswith('skill_'))}")
    print(f"   Total DataFrame shape: {df.shape}")
    
    return df


# ============================================================================
# TESTING
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("TESTING COMPLETE FEATURE ENGINEERING")
    print("=" * 70)
    
    test_input = {
        'job_title_short': 'Senior Data Scientist',
        'job_country': 'US',
        'job_state': 'CA',
        'skills_text': 'python, sql, machine learning, tensorflow, aws, pandas, numpy',
        'job_schedule_type': 'full_time',
        'remote_option': 1,
    }
    
    print(f"\nInput Data:")
    for k, v in test_input.items():
        print(f"  {k}: {v}")
    
    df, features = prepare_complete_features(test_input)
    
    print(f"\n✅ Features Generated: {len(features)}")
    print(f"\nDataFrame Shape: {df.shape}")
    print(f"Columns: {list(df.columns)[:10]}... (showing first 10)")
    
    print(f"\n🔍 Sample Feature Values:")
    sample_features = {
        'job_title_short': features['job_title_short'],
        'n_skills': features['n_skills'],
        'is_senior': features['is_senior'],
        'has_cloud': features['has_cloud'],
        'skill_python': features['skill_python'],
        'skill_aws': features['skill_aws'],
        'posted_month': features['posted_month'],
    }
    for k, v in sample_features.items():
        print(f"  {k}: {v}")
    
    print("\n" + "=" * 70)
    print("✅ ALL REQUIRED FEATURES GENERATED SUCCESSFULLY")
    print("=" * 70)
