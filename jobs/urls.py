from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Job seeker URLs
    path('', views.job_list_view, name='job_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('<int:job_id>/apply/', views.apply_job_view, name='apply_job'),
    path('applied/', views.jobs_i_applied_for_view, name='jobs_applied'),
    
    # Employer URLs
    path('add/', views.add_job_view, name='add_job'),
    path('my-jobs/', views.my_jobs_view, name='my_jobs'),
]
