from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.permissions import employer_required, job_seeker_required
from accounts.models import EmployerProfile, JobSeekerProfile
from .models import Job, JobApplication
from .forms import JobForm


# ===== EMPLOYER VIEWS =====

@login_required
@employer_required
def add_job_view(request):
    """Employer can post a new job"""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.employer_profile
            job.save()
            messages.success(request, 'Job posted successfully! It will be visible once approved by admin.')
            return redirect('jobs:my_jobs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})


@login_required
@employer_required
def my_jobs_view(request):
    """List all jobs posted by the logged-in employer"""
    jobs = Job.objects.filter(company=request.user.employer_profile)
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})


# ===== JOB SEEKER VIEWS =====

@login_required
@job_seeker_required
def job_list_view(request):
    """List all approved jobs for job seekers"""
    jobs = Job.objects.filter(approved=True)
    
    # Optional: Add search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(company__company_name__icontains=search_query)
        )
    
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'search_query': search_query})


@login_required
@job_seeker_required
def job_detail_view(request, job_id):
    """Detail page for a specific job"""
    job = get_object_or_404(Job, id=job_id, approved=True)
    
    # Check if user has already applied
    has_applied = JobApplication.objects.filter(
        job=job,
        applicant=request.user.jobseeker_profile
    ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })


@login_required
@job_seeker_required
def apply_job_view(request, job_id):
    """Apply for a job"""
    job = get_object_or_404(Job, id=job_id, approved=True)
    applicant = request.user.jobseeker_profile
    
    # Check if already applied
    if JobApplication.objects.filter(job=job, applicant=applicant).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', job_id=job.id)
    
    if request.method == 'POST':
        JobApplication.objects.create(
            job=job,
            applicant=applicant,
            status='pending'
        )
        messages.success(request, f'Successfully applied for {job.title}!')
        return redirect('jobs:jobs_applied')
    
    return redirect('jobs:job_detail', job_id=job.id)


@login_required
@job_seeker_required
def jobs_i_applied_for_view(request):
    """List of jobs the user has applied for"""
    applications = JobApplication.objects.filter(
        applicant=request.user.jobseeker_profile
    ).select_related('job', 'job__company')
    
    return render(request, 'jobs/jobs_i_applied_for.html', {'applications': applications})
