from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    #path('job-seekers/', views.job_seeker_predictions_view, name='job_seeker_predictions'),
    #path('employers/', views.employer_predictions_view, name='employer_predictions'),
     path("health-insurance/", views.health_insurance_view, name="health_insurance"),
]
