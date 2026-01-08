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
        'powerbi_embed_url': 'https://app.powerbi.com/reportEmbed?reportId=333d3265-91dd-4f14-85ee-480280f0b9a0&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730',
    }
    return render(request, 'analytics/powerbi_dashboard.html', context)
