from django.db import models
from accounts.models import User, EmployerProfile, JobSeekerProfile


class Job(models.Model):
    """Job posting model"""
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('none', 'No Specific Requirement'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True, help_text='Job requirements and qualifications')
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    company_description = models.TextField(blank=True, null=True, help_text='Brief company description')
    company_website = models.URLField(blank=True, null=True, help_text='Company website URL')
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    skills_required = models.TextField(blank=True, null=True, help_text='Required skills (comma-separated)')
    degree_required = models.BooleanField(default=False, null=True, blank=True)
    remote_option = models.BooleanField(default=False, null=True, blank=True)
    benefits = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True, help_text='Application deadline')
    posted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-posted_at']
    
    def __str__(self):
        return f"{self.title} at {self.company.company_name}"
    
    def get_applicants_count(self):
        """Return number of applicants for this job"""
        return self.applications.count()


class JobApplication(models.Model):
    """Job application model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']
    
    def __str__(self):
        return f"{self.applicant.user.get_full_name()} applied for {self.job.title}"
