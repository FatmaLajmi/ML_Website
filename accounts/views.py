from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm, SignupForm, EmployerProfileForm, JobSeekerProfileForm
from .models import User


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Redirect superuser directly to admin page
                if user.is_superuser:
                    return redirect('admin:index')
                
                return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def signup_view(request):
    """Handle user signup with role-based profile creation"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to JobML Platform, {user.get_full_name()}!')
            return redirect('accounts:dashboard_redirect')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    """Display and edit user profile"""
    user = request.user
    profile = user.get_profile()
    
    if request.method == 'POST':
        if user.role == 'employer':
            form = EmployerProfileForm(request.POST, instance=profile)
        elif user.role == 'job_seeker':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            messages.error(request, 'Invalid user role.')
            return redirect('accounts:profile')
        
        if form.is_valid():
            profile_instance = form.save(commit=False)
            profile_instance.user = user  # Ensure user is set
            profile_instance.save()
            
            # For job seekers, save the many-to-many skills field
            if user.role == 'job_seeker':
                form.save_m2m()
            
            # Update user info
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if user.role == 'employer':
            form = EmployerProfileForm(instance=profile)
        elif user.role == 'job_seeker':
            form = JobSeekerProfileForm(instance=profile)
        else:
            form = None
    
    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_redirect_view(request):
    """Redirect users to appropriate dashboard based on role"""
    user = request.user
    
    # Check if user is superuser first
    if user.is_superuser:
        return redirect('admin:index')  # Admin dashboard
    
    if user.role == 'employer':
        return redirect('home')  # Redirect to home
    elif user.role == 'job_seeker':
        return redirect('home')  # Redirect to home
    elif user.role == 'admin':
        return redirect('admin:index')  # Admin dashboard
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('home')


def page_view(request):
    """Generic page view (can be used for terms, privacy, etc.)"""
    return render(request, 'accounts/page.html')