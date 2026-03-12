from django.shortcuts import render, redirect
from .models import Paper
from colleges.models import College, Stream
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def dashboard(request):
    colleges = College.objects.all()
    return render(request, 'dashboard.html', {'colleges': colleges})

def paper_search(request):
    papers = Paper.objects.all().order_by('-year') # Shows latest papers first
    
    college_id = request.GET.get('college')
    stream_id = request.GET.get('stream')
    sem = request.GET.get('semester')
    year = request.GET.get('year') # New line

    if college_id:
        papers = papers.filter(college_id=college_id)
    if stream_id:
        papers = papers.filter(stream_id=stream_id)
    if sem:
        papers = papers.filter(semester=sem)
    if year: # New line
        papers = papers.filter(year=year)

    # Generate a list of years for the dropdown (e.g., last 10 years)
    import datetime
    current_year = datetime.datetime.now().year
    year_range = range(current_year, current_year - 10, -1)

    context = {
        'papers': papers,
        'colleges': College.objects.all(),
        'streams': Stream.objects.all(),
        'year_range': year_range, # New line
    }
    return render(request, 'papers.html', context)

from django.contrib import messages

@login_required
def upload_paper(request):
    # 1. Check if profile exists
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Account error: Profile not found.")
        return redirect('dashboard')

    # 2. Check for Faculty + Verification
    if request.user.profile.role == 'FACULTY' and request.user.profile.is_verified:
        form = Paper()
        return render(request, 'upload.html', {'form': form})
    
    # 3. If not verified, send a Warning Message
    else:
        messages.warning(request, "Verification Pending: Your faculty account is currently under review by the WB Academic Board.")
        return redirect('dashboard')