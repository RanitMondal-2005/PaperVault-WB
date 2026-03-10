from django.shortcuts import render, redirect
from .models import Paper
from colleges.models import College, Stream
from django.contrib.auth.decorators import login_required

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

@login_required
def upload_paper(request):
    if request.user.profile.role != 'FACULTY':
        return redirect('dashboard')
    
    if request.method == "POST":
        # Professional implementation would use a Django Form
        title = request.POST.get('title')
        file = request.FILES.get('pdf')
        # ... logic to save paper ...
        return redirect('papers')
    
    return render(request, 'upload.html')