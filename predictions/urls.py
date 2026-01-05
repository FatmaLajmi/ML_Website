from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('job-seekers/', views.job_seeker_predictions_view, name='job_seeker_predictions'),
    path('employers/', views.employer_predictions_view, name='employer_predictions'),
    path('degree-mention/', views.degree_mention_view, name='degree_mention'),
    path("remote-work/", views.remote_work_page, name="remote_work"),
    # path('employer-growth/', views.employer_growth_view, name='employer_growth'),  # Removed - now handled by modal
]
