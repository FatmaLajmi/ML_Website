from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('post/', views.post_job_view, name='post_job'),
    path('my-jobs/', views.my_jobs_view, name='my_jobs'),
    path('<int:job_id>/edit/', views.edit_job_view, name='edit_job'),
    path('<int:job_id>/delete/', views.delete_job_view, name='delete_job'),
    path('<int:job_id>/apply/', views.apply_job_view, name='apply_job'),
    path('applied/', views.jobs_applied_view, name='jobs_applied'),
    path('<int:job_id>/applications/', views.job_applications_view, name='job_applications'),
]
