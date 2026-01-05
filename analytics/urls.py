from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.powerbi_dashboard_view, name='powerbi_dashboard'),
]
