from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    """Model for skills that job seekers can have"""
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_profile(self):
        """Get the appropriate profile based on role"""
        if self.role == 'employer':
            return getattr(self, 'employer_profile', None)
        elif self.role == 'job_seeker':
            return getattr(self, 'jobseeker_profile', None)
        return None


class EmployerProfile(models.Model):
    """Profile for employers"""
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001+', '1001+ employees'),
    ]
    
    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('consulting', 'Consulting'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES)
    website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"


class JobSeekerProfile(models.Model):
    """Profile for job seekers"""
    EDUCATION_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor Degree'),
        ('master', 'Master Degree'),
        ('phd', 'PhD'),
        ('bootcamp', 'Bootcamp'),
        ('self_taught', 'Self-Taught'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES)
    years_experience = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, related_name='job_seekers', blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.username}"
    
    def get_skills_list(self):
        """Return comma-separated list of skills"""
        return ", ".join([skill.name for skill in self.skills.all()])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile when user is created (only if profile doesn't exist)"""
    # Note: Profile creation is now handled by the signup form
    # This signal is kept for backwards compatibility with admin or other creation methods
    if created:
        if instance.role == 'employer':
            # Only create if profile doesn't exist (to allow form to create with data)
            if not hasattr(instance, 'employer_profile'):
                EmployerProfile.objects.get_or_create(
                    user=instance,
                    defaults={
                        'company_name': f"{instance.username}'s Company",
                        'industry': 'technology',
                        'company_size': '1-10'
                    }
                )
        elif instance.role == 'job_seeker':
            # Only create if profile doesn't exist (to allow form to create with data)
            if not hasattr(instance, 'jobseeker_profile'):
                JobSeekerProfile.objects.get_or_create(
                    user=instance,
                    defaults={
                        'education_level': 'bachelor',
                        'years_experience': 0
                    }
                )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if instance.role == 'employer' and hasattr(instance, 'employer_profile'):
        instance.employer_profile.save()
    elif instance.role == 'job_seeker' and hasattr(instance, 'jobseeker_profile'):
        instance.jobseeker_profile.save()
