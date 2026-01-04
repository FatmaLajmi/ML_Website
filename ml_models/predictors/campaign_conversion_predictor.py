"""
Campaign Conversion Prediction Module
Predicts whether marketing campaigns will have high or low conversion rates
"""
import pandas as pd
import numpy as np
from ..models_loader import models_loader


class CampaignConversionPredictor:
    """Campaign conversion prediction handler"""
    
    def __init__(self):
        self.model = models_loader.get_model('campaign_conversion')
        self.scaler = models_loader.get_model('campaign_scaler')
        
        # If scaler doesn't exist, create a simple one based on typical campaign durations
        # Assuming typical campaigns range from 1-90 days with mean ~30
        if self.scaler is None:
            print("WARNING: Scaler not found, using default scaling for Duration")
            # We'll use manual scaling: (x - mean) / std
            # Based on typical campaign data: mean=30, std=20
            self.duration_mean = 30.0
            self.duration_std = 20.0
    
    def predict(self, input_data):
        """
        Predict campaign conversion (High or Low)
        Args:
            input_data: Dictionary with keys:
                - company (str)
                - campaign_type (str)
                - target_audience (str)
                - duration (int)
                - channel_used (str)
                - location (str)
                - language (str)
                - customer_segment (str)
        Returns:
            Dictionary with prediction results
        """
        # Check if model is loaded
        if self.model is None:
            return {'error': 'Campaign conversion prediction model is not available'}
        
        try:
            # Prepare features
            features = self._prepare_features(input_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            prediction_proba = self.model.predict_proba(features)[0]
            
            # Convert to label
            prediction_label = 'High' if prediction == 1 else 'Low'
            confidence = float(prediction_proba[prediction]) * 100
            
            # Get recommendations
            recommendations = self._generate_recommendations(
                input_data, 
                prediction_label, 
                confidence
            )
            
            result = {
                'success': True,
                'prediction': prediction_label,
                'confidence': round(confidence, 2),
                'probability_high': round(float(prediction_proba[1]) * 100, 2),
                'probability_low': round(float(prediction_proba[0]) * 100, 2),
                'recommendations': recommendations,
                'input_data': input_data
            }
            
            return result
            
        except Exception as e:
            return {'error': f'Prediction error: {str(e)}'}
    
    def _prepare_features(self, input_data):
        """
        Prepare features for the model
        The model expects one-hot encoded categorical features with scaled Duration
        NOTE: Company and Location are NOT used (removed for generalization)
        """
        # Create a DataFrame with the input (NO Company or Location)
        df = pd.DataFrame([{
            'Campaign_Type': input_data.get('campaign_type', ''),
            'Target_Audience': input_data.get('target_audience', ''),
            'Channel_Used': input_data.get('channel_used', ''),
            'Language': input_data.get('language', ''),
            'Customer_Segment': input_data.get('customer_segment', ''),
            'Duration': int(input_data.get('duration', 30))
        }])
        
        print(f"DEBUG - Input data: {input_data}")
        
        # Define categorical columns (NO Company or Location)
        categorical_cols = ['Campaign_Type', 'Target_Audience', 
                          'Channel_Used', 'Language', 'Customer_Segment']
        
        # One-hot encode
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        print(f"DEBUG - Encoded features: {df_encoded.columns.tolist()}")
        print(f"DEBUG - Duration before scaling: {df_encoded['Duration'].values[0]}")
        
        # Get expected features from the model
        if hasattr(self.model, 'feature_names_in_'):
            expected_features = list(self.model.feature_names_in_)
            print(f"DEBUG - Model expects {len(expected_features)} features")
        else:
            expected_features = df_encoded.columns.tolist()
        
        # Scale Duration BEFORE aligning features
        if 'Duration' in df_encoded.columns:
            original_duration = df_encoded['Duration'].values[0]
            if self.scaler is not None:
                try:
                    df_encoded['Duration'] = self.scaler.transform(df_encoded[['Duration']])
                    print(f"DEBUG - Duration scaled from {original_duration} to {df_encoded['Duration'].values[0]}")
                except Exception as e:
                    print(f"DEBUG - Scaling failed: {e}")
                    df_encoded['Duration'] = (df_encoded['Duration'] - 30) / 20
            else:
                # Manual scaling if no scaler
                df_encoded['Duration'] = (df_encoded['Duration'] - 30) / 20
                print(f"DEBUG - Duration manually scaled from {original_duration} to {df_encoded['Duration'].values[0]}")
        
        # Create final DataFrame with all expected features
        final_df = pd.DataFrame(columns=expected_features)
        for col in expected_features:
            if col in df_encoded.columns:
                final_df[col] = df_encoded[col].values
            else:
                final_df[col] = 0
        
        print(f"DEBUG - Final shape: {final_df.shape}")
        non_zero = [(col, val) for col, val in final_df.iloc[0].items() if val != 0]
        print(f"DEBUG - Active features: {non_zero}")
        
        return final_df
        """
        Prepare features for the model
        The model expects one-hot encoded categorical features with scaled Duration
        """
        # Create a DataFrame with the input
        df = pd.DataFrame([{
            'Company': input_data.get('company', ''),
            'Campaign_Type': input_data.get('campaign_type', ''),
            'Target_Audience': input_data.get('target_audience', ''),
            'Channel_Used': input_data.get('channel_used', ''),
            'Location': input_data.get('location', ''),
            'Language': input_data.get('language', ''),
            'Customer_Segment': input_data.get('customer_segment', ''),
            'Duration': int(input_data.get('duration', 30))
        }])
        
        # Debug: Print input
        print(f"DEBUG - Input data: {input_data}")
        
        # Define categorical columns
        categorical_cols = ['Company', 'Campaign_Type', 'Target_Audience', 
                          'Channel_Used', 'Location', 'Language', 'Customer_Segment']
        
        # One-hot encode
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        print(f"DEBUG - Encoded features: {df_encoded.columns.tolist()}")
        print(f"DEBUG - Duration before scaling: {df_encoded['Duration'].values[0]}")
        
        # Get expected features from the model
        if hasattr(self.model, 'feature_names_in_'):
            expected_features = list(self.model.feature_names_in_)
            print(f"DEBUG - Model expects {len(expected_features)} features")
            print(f"DEBUG - Expected features: {expected_features[:10]}...")  # Print first 10
        else:
            print("WARNING - Model does not have feature_names_in_, using current features")
            expected_features = df_encoded.columns.tolist()
        
        # Scale Duration BEFORE aligning features (this is how training did it)
        if 'Duration' in df_encoded.columns:
            original_duration = df_encoded['Duration'].values[0]
            if self.scaler is not None:
                try:
                    df_encoded['Duration'] = self.scaler.transform(df_encoded[['Duration']])
                    print(f"DEBUG - Duration after scaling: {df_encoded['Duration'].values[0]}")
                except Exception as e:
                    print(f"DEBUG - Scaling failed: {e}, using manual scaling")
                    # Manual scaling as fallback
                    df_encoded['Duration'] = (df_encoded['Duration'] - self.duration_mean) / self.duration_std
                    print(f"DEBUG - Duration manually scaled from {original_duration} to {df_encoded['Duration'].values[0]}")
            else:
                # Use manual scaling
                df_encoded['Duration'] = (df_encoded['Duration'] - self.duration_mean) / self.duration_std
                print(f"DEBUG - Duration manually scaled from {original_duration} to {df_encoded['Duration'].values[0]}")
        
        # Add missing columns with 0 (for features not in current input)
        for col in expected_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        # Remove extra columns not in expected features
        df_encoded = df_encoded[[col for col in expected_features if col in df_encoded.columns or col in expected_features]]
        
        # Ensure all expected features are present in correct order
        final_df = pd.DataFrame(columns=expected_features)
        for col in expected_features:
            if col in df_encoded.columns:
                final_df[col] = df_encoded[col].values
            else:
                final_df[col] = 0
        
        print(f"DEBUG - Final feature shape: {final_df.shape}")
        print(f"DEBUG - Non-zero features: {[(col, val) for col, val in final_df.iloc[0].items() if val != 0]}")
        
        return final_df
    
    def _get_all_possible_features(self):
        """
        Get all possible features based on the form choices
        This recreates the feature names that would be generated during training
        """
        # All possible values from the form (need to match training data)
        companies = []  # We don't know all companies, this might need adjustment
        campaign_types = ['Email', 'Influencer', 'Search', 'Social Media']
        target_audiences = ['All Ages', 'Men 18-24', 'Men 25-34', 'Women 25-34', 'Women 35-44']
        channels = ['Email', 'Facebook', 'Google Ads', 'Instagram', 'Website', 'YouTube']
        locations = []  # We don't know all locations
        languages = ['English', 'French', 'Spanish', 'Mandarin', 'German']
        segments = ['Fashionistas', 'Health & Wellness', 'Outdoor Adventures', 'Foodies', 'Tech Enthusiasts']
        
        features = ['Duration']  # Start with numeric feature
        
        # Add one-hot encoded features (drop_first=True means first alphabetically is dropped)
        # Campaign_Type (drop Email as it's first alphabetically)
        for val in sorted(campaign_types)[1:]:
            features.append(f'Campaign_Type_{val}')
        
        # Target_Audience (drop All Ages)
        for val in sorted(target_audiences)[1:]:
            features.append(f'Target_Audience_{val}')
        
        # Channel_Used (drop Email)
        for val in sorted(channels)[1:]:
            features.append(f'Channel_Used_{val}')
        
        # Language (drop English)
        for val in sorted(languages)[1:]:
            features.append(f'Language_{val}')
        
        # Customer_Segment (drop Fashionistas)
        for val in sorted(segments)[1:]:
            features.append(f'Customer_Segment_{val}')
        
        # Note: Company and Location are dynamic and would need to be handled
        # based on the actual training data. For now, we'll let the model handle missing features
        
        return features
    
    def _generate_recommendations(self, input_data, prediction, confidence):
        """Generate actionable recommendations based on prediction"""
        recommendations = []
        
        if prediction == 'High':
            recommendations.append(f"✓ Your campaign is predicted to have HIGH conversion rates ({confidence:.1f}% confidence)")
            recommendations.append("✓ Continue with your current campaign strategy")
            recommendations.append("✓ Consider scaling up the budget to maximize ROI")
            
            # Channel-specific recommendations
            channel = input_data.get('channel_used', '')
            if channel.lower() in ['google ads', 'facebook']:
                recommendations.append(f"✓ {channel} is performing well for your target audience")
            
        else:
            recommendations.append(f"⚠ Your campaign is predicted to have LOW conversion rates ({confidence:.1f}% confidence)")
            recommendations.append("⚠ Consider revising your campaign strategy")
            
            # Provide specific suggestions
            channel = input_data.get('channel_used', '')
            target = input_data.get('target_audience', '')
            
            # Channel recommendations
            if channel.lower() == 'email':
                recommendations.append("💡 Try complementing email with social media ads for better reach")
            elif channel.lower() in ['facebook', 'instagram']:
                recommendations.append("💡 Consider A/B testing different ad creatives")
            
            # Duration recommendations
            duration = int(input_data.get('duration', 30))
            if duration < 14:
                recommendations.append("💡 Consider extending campaign duration to at least 14-30 days")
            elif duration > 60:
                recommendations.append("💡 Break long campaigns into smaller, targeted phases")
            
            # Target audience recommendations
            if 'all ages' in target.lower():
                recommendations.append("💡 Segment your audience for more targeted messaging")
            
            recommendations.append("💡 Review your customer segment alignment with the campaign type")
        
        return recommendations


# Create a singleton instance
campaign_conversion_predictor = CampaignConversionPredictor()
