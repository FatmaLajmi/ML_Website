"""
Job Title Prediction Module
Predicts suitable job titles based on user skills and experience
Uses job_classifier_model. pkl with feature engineering
"""
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.sparse import hstack, csr_matrix


class JobTitlePredictor:  
    """Job title prediction handler using job_classifier_model.pkl"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self. discriminative_skills = []
        self.feature_config = {}
        self.metadata = {}
        self._load_model()
        self._load_config_files()
    
    def _load_model(self):
        """Load the job classifier model"""
        try:  
            models_dir = Path(__file__).parent.parent / 'models'
            model_path = models_dir / 'job_classifier_model.pkl'
            
            print(f"Looking for job title model in: {models_dir}")
            print(f"Model path: {model_path}")
            print(f"Model exists: {model_path.exists()}")
            
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    artifacts = pickle.load(f)
                    
                    # Load all artifacts
                    self.model = artifacts['model']
                    self. vectorizer = artifacts['vectorizer']
                    self.label_encoder = artifacts['label_encoder']
                    self.discriminative_skills = artifacts. get('discriminative_skills', [])
                    self.metadata = artifacts.get('model_metadata', {})
                    
                print("✅ Job title classifier model loaded successfully")
                print(f"   Model type: {type(self.model)}")
                print(f"   Vectorizer:  {type(self.vectorizer)}")
                print(f"   Classes: {self.label_encoder.classes_}")
            else:
                print(f"❌ Job title model not found at {model_path}")
        except Exception as e:
            print(f"❌ Error loading job title model: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_config_files(self):
        """Load JSON configuration files"""
        try: 
            models_dir = Path(__file__).parent.parent / 'models'
            
            # Load discriminative skills (if not already loaded from model)
            if not self.discriminative_skills:
                disc_skills_path = models_dir / 'discriminative_skills.json'
                if disc_skills_path.exists():
                    with open(disc_skills_path, 'r') as f:
                        self.discriminative_skills = json.load(f)
                    print(f"✓ Loaded {len(self. discriminative_skills)} discriminative skills")
            
            # Load feature engineering config
            feature_config_path = models_dir / 'feature_engineering_config.json'
            if feature_config_path.exists():
                with open(feature_config_path, 'r') as f:
                    self.feature_config = json.load(f)
                print(f"✓ Loaded feature engineering config")
            
            # Load model metadata (if not already loaded)
            if not self.metadata:
                metadata_path = models_dir / 'model_metadata.json'
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        self.metadata = json.load(f)
                    print(f"✓ Loaded model metadata - {self.metadata. get('n_classes', 0)} job classes")
            
        except Exception as e:  
            print(f"⚠️ Warning: Could not load config files: {e}")
    
    def _normalize_skill(self, skill):
        """Normalize skill name for matching"""
        return skill.lower().strip().replace('-', '').replace('_', '').replace(' ', '')
    
    def _determine_seniority_from_experience(self, years_of_experience):
        """
        Determine if role should be senior based on years of experience
        
        Args:
            years_of_experience: Number of years (integer or float)
        
        Returns:
            1 if senior level, 0 if not
        
        Typical seniority thresholds in tech:
        - Junior: 0-2 years
        - Mid-level: 2-5 years
        - Senior: 5+ years
        """
        if years_of_experience is None:
            return 0
        
        try:
            years = float(years_of_experience)
            
            # Senior threshold: 5+ years
            if years >= 5:
                return 1
            else:
                return 0
                
        except (ValueError, TypeError):
            return 0
    
    def _engineer_features(self, skills_list, years_of_experience=None):
        """
        Engineer features from skills list using feature_engineering_config
        Args:
            skills_list: List of skill names
            years_of_experience: Years of experience (for seniority detection)
        Returns: 
            Dictionary of engineered features
        """
        # Normalize skills to lowercase for matching
        skills_lower = [self._normalize_skill(skill) for skill in skills_list]
        
        # Helper function to check if skill matches
        def skill_in_list(skill, reference_list):
            normalized_ref = [self._normalize_skill(ref) for ref in reference_list]
            return any(skill == ref for ref in normalized_ref)
        
        # Determine seniority from years of experience
        is_senior = self._determine_seniority_from_experience(years_of_experience)
        
        # Count programming skills
        prog_skills = sum(1 for skill in skills_lower 
                         if skill_in_list(skill, self.feature_config. get('programming_skills', [])))
        
        # Count cloud skills
        cloud_skills = sum(1 for skill in skills_lower 
                          if skill_in_list(skill, self. feature_config.get('cloud_skills', [])))
        
        # Count ML tools
        ml_skills = sum(1 for skill in skills_lower 
                       if skill_in_list(skill, self.feature_config.get('ml_tools', [])))
        
        # Count visualization tools
        viz_skills = sum(1 for skill in skills_lower 
                        if skill_in_list(skill, self.feature_config.get('viz_tools', [])))
        
        # Count discriminative skills
        discriminative_skills_count = sum(1 for skill in skills_lower 
                                         if skill_in_list(skill, self.discriminative_skills))
        
        # Count big data skills
        big_data_count = sum(1 for skill in skills_lower 
                            if skill_in_list(skill, self.feature_config.get('big_data_skills', [])))
        
        # Count DevOps skills
        devops_count = sum(1 for skill in skills_lower 
                          if skill_in_list(skill, self.feature_config.get('devops_skills', [])))
        
        # Count deep learning skills
        deep_learning_count = sum(1 for skill in skills_lower 
                                 if skill_in_list(skill, self.feature_config.get('deep_learning_skills', [])))
        
        return {
            'is_senior': is_senior,
            'prog_skills': prog_skills,
            'cloud_skills': cloud_skills,
            'ml_skills': ml_skills,
            'viz_skills': viz_skills,
            'discriminative_skills_count': discriminative_skills_count,
            'big_data_count': big_data_count,
            'devops_count': devops_count,
            'deep_learning_count': deep_learning_count
        }
    
    def _get_career_advice(self, job_title, features, years_of_experience):
        """Generate personalized career advice based on role and experience"""
        
        # Skill recommendations based on job title
        skill_map = {
            'Data Scientist': ['Machine Learning', 'Python', 'Statistics', 'TensorFlow', 'PyTorch', 'Deep Learning'],
            'Senior Data Scientist': ['Advanced ML', 'Model Deployment', 'MLOps', 'Team Leadership', 'Research Methods'],
            'Data Engineer': ['Apache Spark', 'Airflow', 'SQL', 'Python', 'ETL', 'Data Warehousing'],
            'Senior Data Engineer': ['Kafka', 'System Design', 'Cloud Architecture', 'Team Leadership', 'Data Governance'],
            'Machine Learning Engineer': ['TensorFlow', 'PyTorch', 'MLOps', 'Docker', 'Kubernetes', 'Model Serving'],
            'Analyst (BA/DA)': ['SQL', 'Tableau', 'Power BI', 'Excel', 'Business Intelligence', 'Data Visualization'],
            'Senior Data Analyst': ['Advanced SQL', 'Python', 'Statistical Analysis', 'Reporting', 'Stakeholder Management'],
            'Cloud Engineer': ['AWS', 'Azure', 'GCP', 'Terraform', 'Kubernetes', 'CI/CD'],
            'Software Engineer': ['Java', 'C++', 'System Design', 'Algorithms', 'Git', 'Testing'],
            'Senior Data Scientist': ['MLOps', 'Team Leadership', 'Architecture', 'Mentoring', 'Strategy']
        }
        
        # Generate advice based on experience level
        advice_map = {
            'Data Scientist': 'Focus on strengthening your statistical and machine learning foundations.  Build a portfolio of real-world projects showcasing your ability to extract insights from data.',
            'Senior Data Scientist': 'As a senior role, emphasize leadership, mentoring, and strategic thinking. Focus on end-to-end project ownership and cross-functional collaboration.',
            'Data Engineer': 'Master data pipeline design and ETL processes. Understanding cloud platforms and distributed systems will significantly boost your career prospects.',
            'Senior Data Engineer': 'Develop expertise in system architecture and scalability. Leadership and mentoring skills are crucial at this level.',
            'Machine Learning Engineer': 'Bridge the gap between ML models and production systems. Focus on MLOps, model deployment, and software engineering best practices.',
            'Analyst (BA/DA)': 'Strengthen your data visualization and storytelling skills. Learn to translate complex data into actionable business insights.',
            'Senior Data Analyst': 'Develop strategic thinking and stakeholder management skills. Consider learning programming (Python/R) to advance your analytical capabilities.',
            'Cloud Engineer':  'Gain multi-cloud expertise and focus on automation.  Infrastructure as Code (IaC) and DevOps practices are essential skills.',
            'Software Engineer': 'Build strong fundamentals in data structures, algorithms, and system design.  Contribute to open-source projects to build your reputation.'
        }
        
        # Add experience-specific advice
        if years_of_experience is not None:
            years = float(years_of_experience)
            if years < 2:
                experience_context = "As someone early in your career, focus on building strong fundamentals and gaining hands-on experience. "
            elif years < 5:
                experience_context = "With your mid-level experience, focus on deepening your expertise and taking on more complex projects. "
            else:
                experience_context = "With your senior-level experience, consider leadership opportunities and mentoring junior team members. "
        else:
            experience_context = ""
        
        recommended_skills = skill_map.get(job_title, ['Python', 'SQL', 'Data Analysis'])
        base_advice = advice_map.get(job_title, 'Continue building your skills and gaining practical experience in your field.')
        
        advice = experience_context + base_advice
        
        return advice, recommended_skills[: 6]
    
    def predict(self, skills_list, years_of_experience=None):
        """
        Predict job title based on skills and experience
        
        Args: 
            skills_list: List of skill names (strings) from user profile
            years_of_experience:  Years of professional experience (integer/float)
                                Determines seniority level: 
                                - 0-2 years: Junior/Mid-level
                                - 2-5 years: Mid-level
                                - 5+ years: Senior level
        
        Returns:
            Dictionary with prediction results
        """
        if self.model is None or self.vectorizer is None:
            return {
                'success': False, 
                'error': 'Job title prediction model is not available'
            }
        
        if not skills_list:  
            return {
                'success': False,
                'error': 'No skills provided',
                'redirect_to_profile': True
            }
        
        try:  
            # Normalize skills for matching with discriminative skills
            skills_normalized = [self._normalize_skill(skill) for skill in skills_list]
            discriminative_normalized = [self._normalize_skill(skill) for skill in self.discriminative_skills]
            
            # Filter to only discriminative skills (like training)
            discriminative_used = []
            for i, norm_skill in enumerate(skills_normalized):
                if norm_skill in discriminative_normalized:  
                    discriminative_used.append(skills_list[i])  # Keep original casing
            
            # Create skills text using ONLY discriminative skills
            skills_text = ' '.join([self._normalize_skill(s) for s in discriminative_used])
            
            print(f"📝 Input skills: {skills_list}")
            print(f"👤 Years of experience: {years_of_experience}")
            print(f"🎯 Discriminative skills matched: {discriminative_used}")
            print(f"📄 Skills text for vectorizer: '{skills_text}'")
            
            # Vectorize the skills using TF-IDF (MUST use discriminative skills only!)
            X_vec = self.vectorizer.transform([skills_text])
            
            # Engineer additional features (now includes experience-based seniority)
            engineered_features = self._engineer_features(skills_list, years_of_experience)
            
            # Feature order (must match training!)
            feature_order = [
                'is_senior', 'prog_skills', 'cloud_skills', 'ml_skills', 'viz_skills',
                'discriminative_skills_count', 'big_data_count', 'devops_count', 'deep_learning_count'
            ]
            
            # Create feature array in correct order
            X_add = np.array([[engineered_features[f] for f in feature_order]])
            
            print(f"🔢 Engineered features:  {engineered_features}")
            print(f"   → is_senior = {engineered_features['is_senior']} (based on {years_of_experience} years)")
            
            # Combine TF-IDF + engineered features (like training!)
            X_final = hstack([X_vec, csr_matrix(X_add)])
            
            print(f"✅ Final feature shape: {X_final.shape}")
            
            # Make prediction
            prediction_encoded = self.model.predict(X_final)[0]
            prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
            
            print(f"🎯 Prediction: {prediction}")
            
            # Get probabilities
            probabilities_array = self.model.predict_proba(X_final)[0]
            confidence = max(probabilities_array)
            
            # Get top 3 predictions
            top_indices = probabilities_array.argsort()[-3:][::-1]
            all_classes = self.label_encoder.classes_
            
            probabilities = [
                {
                    'title': all_classes[idx],
                    'probability': f"{probabilities_array[idx] * 100:.1f}%"
                }
                for idx in top_indices
            ]
            
            print(f"📊 Top 3: {probabilities}")
            
            # Format accuracy
            accuracy = self.metadata.get('accuracy', 0)
            if isinstance(accuracy, float) and accuracy <= 1:
                accuracy_display = f"{accuracy * 100:.1f}%"
            else:
                accuracy_display = str(accuracy)
            
            # Get career advice (now includes experience-aware advice)
            advice, recommended_skills = self._get_career_advice(
                prediction, 
                engineered_features,
                years_of_experience
            )
            
            return {
                'success': True,
                'prediction': prediction,
                'recommended_title': prediction,
                'confidence': f"{confidence * 100:.1f}%",
                'skills_used': skills_list,
                'discriminative_skills_used': discriminative_used,
                'top_predictions': probabilities,
                'advice': advice,
                'recommended_skills': recommended_skills,
                'experience_level': 'Senior' if engineered_features['is_senior'] == 1 else 'Mid-Level',
                'years_of_experience': years_of_experience
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Prediction failed: {str(e)}'
            }


# Global predictor instance
job_title_predictor = JobTitlePredictor()