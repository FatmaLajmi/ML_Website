from django.contrib import admin
from .models import CampaignPrediction


@admin.register(CampaignPrediction)
class CampaignPredictionAdmin(admin.ModelAdmin):
    list_display = ['company', 'campaign_type', 'channel_used', 'prediction', 'confidence', 'user', 'created_at']
    list_filter = ['prediction', 'campaign_type', 'channel_used', 'created_at']
    search_fields = ['company', 'user__username', 'location']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Campaign Details', {
            'fields': ('user', 'company', 'campaign_type', 'target_audience', 'channel_used')
        }),
        ('Campaign Parameters', {
            'fields': ('duration', 'location', 'language', 'customer_segment')
        }),
        ('Prediction Results', {
            'fields': ('prediction', 'confidence', 'probability_high', 'probability_low')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

