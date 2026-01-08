from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def powerbi_dashboard_view(request):
    """Display Power BI dashboard for employers"""
    # Only allow employers to access
    if request.user.role != 'employer':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Only employers can access the analytics dashboard.')
        return redirect('home')
    
    context = {
        'user': request.user,
    }
    return render(request, 'analytics/powerbi_dashboard.html', context)
