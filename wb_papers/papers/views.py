from django.shortcuts import render, redirect
from .models import Paper
from .forms import PaperUploadForm 
from colleges.models import College, Stream
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

def dashboard(request):
    colleges = College.objects.all()
    return render(request, 'dashboard.html', {'colleges': colleges})

def paper_search(request):
    papers = Paper.objects.all().order_by('-year')
    college_id = request.GET.get('college')
    stream_id = request.GET.get('stream')
    sem = request.GET.get('semester')
    year = request.GET.get('year')

    if college_id: papers = papers.filter(college_id=college_id)
    if stream_id: papers = papers.filter(stream_id=stream_id)
    if sem: papers = papers.filter(semester=sem)
    if year: papers = papers.filter(year=year)

    current_year = datetime.datetime.now().year
    year_range = range(current_year, current_year - 10, -1)

    context = {
        'papers': papers,
        'colleges': College.objects.all(),
        'streams': Stream.objects.all(),
        'year_range': year_range,
    }
    return render(request, 'papers.html', context)

@login_required
def upload_paper(request):
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Account error: Profile not found.")
        return redirect('dashboard')    
    
    if request.user.profile.role == 'FACULTY' and request.user.profile.is_verified:
        if request.method == 'POST':
            form = PaperUploadForm(request.POST, request.FILES)
            if form.is_valid():
                paper = form.save(commit=False)
                paper.uploaded_by = request.user
                paper.save()
                messages.success(request, "Paper successfully published!")
                return redirect('dashboard')
        else:
            form = PaperUploadForm()          
        
        return render(request, 'upload.html', {'form': form})
    
    else:
        messages.warning(request, "Verification Pending: Access Denied.")
        return redirect('dashboard')