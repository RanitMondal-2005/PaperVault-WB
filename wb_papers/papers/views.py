from django.shortcuts import render, redirect,get_object_or_404
from .models import Paper
from .forms import PaperUploadForm 
from colleges.models import College, Stream
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .ai_utils import extract_text_from_pdf, get_gemini_analysis


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

    # ---- Applying Paginator Logic -----
    paginator = Paginator(papers, 10) # 10 papers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    current_year = datetime.datetime.now().year
    year_range = range(current_year, current_year - 10, -1)

    context = {
        'papers': page_obj,
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
                messages.error(request, "Error publishing paper.")
        else:
            form = PaperUploadForm()          
        
        return render(request, 'upload.html', {'form': form})
    
    else:
        messages.warning(request, "Verification Pending: Access Denied.")
        return redirect('dashboard')

# Password change Logic
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This is the key: prevents logging the user out after change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)  
    return render(request, 'password_change.html', {'form': form})

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

# ----------- AI INTEGRATION -------------

def ai_lab_dashboard(request):
    # Step 1: Initial Filter Form
    colleges = Paper.objects.values_list('college__name', flat=True).distinct()
    streams = Stream.objects.all()
    return render(request, 'ai_lab_form.html', {
        'colleges': colleges,
        'streams': streams
    })

def ai_select_subject(request):
    """ Intermediate step to find valid subjects based on filters """
    if request.method == 'POST':
        task = request.POST.get('task_type')
        
        # If user chose manual PDF upload, skip straight to analysis
        if task == 'pdf_upload':
            return ai_analyze(request)

        # Get filter data
        start = request.POST.get('start_year')
        end = request.POST.get('end_year')
        sem = request.POST.get('semester')
        institution_name = request.POST.get('institution')
        stream_id = request.POST.get('stream')

        # Find all unique subjects that actually exist for these filters
        papers = Paper.objects.filter(year__range=(start, end), semester=sem)
        if institution_name != 'All':
            papers = papers.filter(college__name=institution_name)
        if stream_id != 'All':
            papers = papers.filter(stream_id=stream_id)

        # Using QuerySets in Django
        subjects = papers.values(
            'subject_name', 
            'subject_code', 
            'year', 
        ).distinct().order_by('-year')

        return render(request, 'ai_select_subject.html', {
            'subjects': subjects,
            'task': task,
            'filters': request.POST # Pass filters forward
        })
    return redirect('ai_lab')

def ai_analyze(request):
    if request.method == 'POST':
        task = request.POST.get('task_type')
        combined_text = ""

        # Logic for stored papers
        if task in ['topics', 'summary','mock_test']:
            subject_name = request.POST.get('selected_subject')
            papers = Paper.objects.filter(
                subject_name=subject_name,
                year__range=(request.POST.get('start_year'), request.POST.get('end_year')),
                semester=request.POST.get('semester')
            )
            for paper in papers[:5]:
                combined_text += extract_text_from_pdf(paper.pdf_file)
        
        # Logic for manual uploads
        elif task == 'pdf_upload':
            for slot in ['pdf1', 'pdf2', 'pdf3']:
                f = request.FILES.get(slot)
                if f:
                    combined_text += extract_text_from_pdf(f)

        # Execution
        if not combined_text.strip():
            return render(request, 'ai_result.html', {'result': "Error: No text could be extracted. Please check your files or selection."})

        # Single API call - task parameter will determine the prompt and analysis style in ai_utils.py
        result = get_gemini_analysis(combined_text, task)

        return render(request, 'ai_result.html', {'result': result, 'task': task})
    
    return redirect('ai_lab')
