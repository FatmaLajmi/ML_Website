from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(allowed_roles):
    """
    Decorator to restrict access based on user role.
    Usage: @role_required(['employer']) or @role_required(['job_seeker', 'employer'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('accounts:page')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def employer_required(view_func):
    """Decorator to restrict access to employers only"""
    return role_required(['employer'])(view_func)


def job_seeker_required(view_func):
    """Decorator to restrict access to job seekers only"""
    return role_required(['job_seeker'])(view_func)
