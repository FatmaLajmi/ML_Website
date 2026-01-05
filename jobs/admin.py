from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'approved', 'posted_at', 'get_applicants_count']
    list_filter = ['approved', 'job_type', 'posted_at', 'degree_required', 'remote_option']
    search_fields = ['title', 'description', 'company__company_name', 'location']
    list_editable = ['approved']
    readonly_fields = ['posted_at']
    ordering = ['-posted_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'description', 'location')
        }),
        ('Job Details', {
            'fields': ('job_type', 'salary_range', 'degree_required', 'remote_option', 'benefits')
        }),
        ('Status', {
            'fields': ('approved', 'posted_at')
        }),
    )
    
    def get_applicants_count(self, obj):
        return obj.get_applicants_count()
    get_applicants_count.short_description = 'Applications'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'job_title', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__user__username', 'applicant__user__email']
    list_editable = ['status']
    readonly_fields = ['applied_at']
    ordering = ['-applied_at']
    
    def applicant_name(self, obj):
        return obj.applicant.user.get_full_name() or obj.applicant.user.username
    applicant_name.short_description = 'Applicant'
    
    def job_title(self, obj):
        return obj.job.title
    job_title.short_description = 'Job'
