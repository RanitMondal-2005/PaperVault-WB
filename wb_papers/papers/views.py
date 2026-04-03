from django.shortcuts import render, redirect,get_object_or_404
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
    
# Implementing Papers Edit and Delete Logic
@login_required
def edit_paper(request, pk):  
    # pk is Primary Key / id , to get the exact row where we will update
    paper = get_object_or_404(Paper, pk=pk)
    
    if paper.uploaded_by != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('papers')

    if request.method == 'POST':
        # NOTE -> Without instance: You have to manually write-> paper.title = request.POST.get('title') and for all other feilds
        form = PaperUploadForm(request.POST, request.FILES, instance=paper)
        # NOTE -> FOR NOW : UPLOADING PDF IS ALSO COMPULSORY -> LATER WE WILL UPDATE IT
        # HACK: If Faculty didn't upload a new pdf file, keep the old one i.e, Updating PDF is optional During Edits
        if not request.FILES.get('pdf_file'):
            form.fields['pdf_file'].required = False
        # Check Forms validation    
        if form.is_valid():
            form.save() # save changes to DB
            messages.success(request, f"Changes saved for {paper.subject_code}!")
            return redirect('dashboard')
    else:
        form = PaperUploadForm(instance=paper)
        # On GET request, the file isn't mandatory to see the page
        # Even if Faculty has those prev uploaded papers in diff device then also they can change/view 
        form.fields['pdf_file'].required = False
    
    return render(request, 'edit_paper.html', {'form': form, 'paper': paper})

@login_required
def delete_paper(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    
    # Security Check
    if paper.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot delete this paper.")
        return redirect('papers')

    if request.method == 'POST':
        paper.delete()
        messages.success(request, "Paper has been permanently removed.")
        return redirect('papers')
    
    return render(request, 'delete_paper.html', {'paper': paper})