from django.shortcuts import render
from jobs.models import Job


def home_view(request):
    """Home page view with latest jobs"""
    # Get latest 6 approved jobs for the home page
    latest_jobs = Job.objects.filter(approved=True)[:6]
    
    context = {
        'latest_jobs': latest_jobs,
    }
    return render(request, 'index.html', context)
