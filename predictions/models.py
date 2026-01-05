from django.db import models
from django.conf import settings


class CampaignPrediction(models.Model):
    """Store campaign conversion predictions for employers"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='campaign_predictions')
    
    # Input data
    company = models.CharField(max_length=200)
    campaign_type = models.CharField(max_length=100)
    target_audience = models.CharField(max_length=100)
    duration = models.IntegerField()
    channel_used = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    language = models.CharField(max_length=50)
    customer_segment = models.CharField(max_length=100)
    
    # Prediction results
    prediction = models.CharField(max_length=10)  # 'High' or 'Low'
    confidence = models.FloatField()
    probability_high = models.FloatField()
    probability_low = models.FloatField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campaign Prediction'
        verbose_name_plural = 'Campaign Predictions'
    
    def __str__(self):
        return f"{self.company} - {self.campaign_type} ({self.prediction})"

