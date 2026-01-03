from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmployerProfile, JobSeekerProfile, Skill


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    """Admin configuration for EmployerProfile model"""
    list_display = ('company_name', 'user', 'industry', 'company_size', 'location', 'created_at')
    list_filter = ('industry', 'company_size', 'created_at')
    search_fields = ('company_name', 'user__username', 'user__email', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Company Information', {
            'fields': ('company_name', 'industry', 'company_size', 'website', 'company_description')
        }),
        ('Contact Information', {
            'fields': ('location', 'contact_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    """Admin configuration for JobSeekerProfile model"""
    list_display = ('get_full_name', 'user', 'education_level', 'years_experience', 'get_skills_preview', 'created_at')
    list_filter = ('education_level', 'years_experience', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('skills',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('education_level', 'years_experience', 'skills', 'bio')
        }),
        ('Contact Information', {
            'fields': ('phone', 'location', 'resume')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Name'
    
    def get_skills_preview(self, obj):
        skills = obj.skills.all()[:3]
        preview = ", ".join([skill.name for skill in skills])
        if obj.skills.count() > 3:
            preview += f" (+{obj.skills.count() - 3} more)"
        return preview or "No skills"
    get_skills_preview.short_description = 'Skills'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin configuration for Skill model"""
    list_display = ('name', 'get_job_seeker_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_job_seeker_count(self, obj):
        return obj.job_seekers.count()
    get_job_seeker_count.short_description = 'Job Seekers'
