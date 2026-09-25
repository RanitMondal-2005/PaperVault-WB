from django.shortcuts import render, redirect, get_object_or_404
from .models import Paper
from .forms import PaperUploadForm
from colleges.models import College, Stream
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .ai_utils import extract_text_from_pdf, get_gemini_analysis


# ------------------ Dashboard ------------------
def dashboard(request):
    colleges = College.objects.all() # Fetch all colleges for the dashboard
    total_papers= Paper.objects.count() # Fetch total no of Q papers currently for the dashboard
    return render(request, 'dashboard.html', {'colleges': colleges,'total_papers':total_papers})


# ------------------ Paper Search Logic ------------
def paper_search(request):
    # Newest papers first i.e. most recent year first shows up first.
    papers = Paper.objects.all().order_by('-year')

    # Grab incoming search parameters from the URL query string (GET parameters)
    college_id = request.GET.get('college')
    stream_id = request.GET.get('stream')
    sem = request.GET.get('semester')
    year = request.GET.get('year')
    exam_type = request.GET.get('exam_type')

    # Filtering Logic : Apply exact matching AND filters
    if college_id: papers = papers.filter(college_id=college_id)
    if stream_id: papers = papers.filter(stream_id=stream_id)
    if sem: papers = papers.filter(semester=sem)
    if year: papers = papers.filter(year=year)
    if exam_type: papers = papers.filter(exam_type=exam_type)

    ### NOTE : By default, chaining multiple .filter() methods or using sequential if statements in Django applies AND to the query. WE ARE ACTUALLY DOING HERE, EXACT MATCHING WITH AND OPERATION FOR ALL FILTERS.

    # Pagination: 10 papers per page
    paginator = Paginator(papers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dropdown year range: from current year down to 2014
    current_year = datetime.date.today().year
    year_range = range(current_year, 2013, -1) # Since we need to dynamically generate Year dropdowns in our Template

    context = {
        'papers': page_obj, # Paginated papers for the current page
        'colleges': College.objects.all(),
        'streams': Stream.objects.all(),
        'year_range': year_range,
    }
    return render(request, 'papers.html', context)


# ------------------ Upload Paper ----------------------------
@login_required
def upload_paper(request):
    # Security Check: Ensure profile exists
    if not hasattr(request.user, 'profile'): # hasattr() -> checks if an object has a specific attribute.Here, it checks if the user has a profile.
        messages.error(request, "Account error: Profile not found.")
        return redirect('dashboard')

    # RBAC: Only verified faculty can publish papers
    if request.user.profile.role == 'FACULTY' and request.user.profile.is_verified:
        if request.method == 'POST':
            form = PaperUploadForm(request.POST, request.FILES) # along with request.POST(i.e, fill the form with user submitted data); request.FILES must be passed explicitly to handle incoming binary PDF data chunks safely
            if form.is_valid(): # Form Validations Check
                paper = form.save(commit=False) # commit=False creates the object instance in memory without saving to the DB immediately, letting us bind the creator ID before executing the final insert query.
                paper.uploaded_by = request.user # This binds the currently logged-in user as the uploader of the paper so that we can track who uploaded each paper.
                paper.save() # Saved to DB
                messages.success(request, "Paper successfully published!")
                return redirect('papers')
            else:
                messages.error(request, "Please correct the highlighted errors below.")
        else:
            form = PaperUploadForm()

        return render(request, 'upload.html', {'form': form})

    else:
        messages.warning(request, "Verification Pending: Access Denied.")
        return redirect('dashboard')


# --------------------- Edit Paper -------------------------------
@login_required
def edit_paper(request, pk):
    # Fetch paper by ID or return 404 if it does not exist
    paper = get_object_or_404(Paper, pk=pk)

    # Security: only the uploader can edit their own paper
    if paper.uploaded_by != request.user:
        messages.error(request, "Unauthorized access.")
        return redirect('papers')

    # Handle form submission
    if request.method == 'POST':
        # instance = paper via POST request: attaches the incoming user edits directly to that existing database record.
        form = PaperUploadForm(request.POST, request.FILES, instance=paper)

        # Make PDF optional so the existing file stays intact if not replaced
        form.fields['pdf_file'].required = False

        if form.is_valid():
            form.save()
            messages.success(request, f"Changes saved for {paper.subject_code}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fix the errors below.")

    else:
        # instance = paper via GET request: display form pre-filled with current paper data
        form = PaperUploadForm(instance=paper)
        form.fields['pdf_file'].required = False

    return render(request, 'edit_paper.html', {'form': form, 'paper': paper})


# ---------------------- Delete Paper ------------------------
@login_required
def delete_paper(request, pk):
    paper = get_object_or_404(Paper, pk=pk)

    if paper.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot delete this paper.")
        return redirect('papers')

    if request.method == 'POST':
        paper.delete()
        messages.success(request, "Paper has been permanently removed.")
        return redirect('papers')

    return render(request, 'delete_paper.html', {'paper': paper})

# ------------------ Password Change Feature (Via Built-in PasswordChangeForm) ------------------
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # This update_session_auth_hash is Session Protection, since Updating the hash keeps the user's active login session valid
            # so changing their password doesn't automatically boot them out of the application.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})


# ------------------------ AI LAB INTEGRATION --------------------------

# ------------- AI DashBoard Page --------------------
def ai_analyzer(request):
    return render(request, 'ai_analyzer.html')


# -------------- Launch AI lab Page -------------------

def ai_lab_dashboard(request):
    # 1. Starts from the Paper table (so colleges with zero papers are ignored).
    #  .values_list('college__name', ...) Goes across the FK to grab ONLY the college's name column, not the whole paper row.
    colleges = Paper.objects.values_list('college__name', flat=True).distinct() # flat=True returns a 1D list of text strings instead of list of tuples

    # 2. All streams with their college info for JS filtering
    streams = Stream.objects.all()

    return render(request, 'ai_lab_form.html', {
        'colleges': colleges,
        'streams': streams
    })


# ------------ Subjects Choice based on Year Range ------------
def ai_select_subject(request):
    if request.method == 'POST':
        task = request.POST.get('task_type')

        # Direct manual PDF uploads skip database subject selection
        if task == 'pdf_upload':
            return ai_analyze(request)

        # 1. Extract Given Input values
        start = request.POST.get('start_year', '').strip()
        end = request.POST.get('end_year', '').strip()
        sem = request.POST.get('semester', '').strip()
        institution = request.POST.get('institution', '').strip()
        stream_id = request.POST.get('stream', '').strip()
        exam_type = request.POST.get('exam_type', '').strip()

        # 2. Year Validation
        current_year = datetime.date.today().year
        try:
            start_year = int(start)
            end_year = int(end)
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid start and end years.")
            return redirect('ai_lab')

        if not (2014 <= start_year <= current_year):
            messages.error(request, f"Start year must be between 2014 and {current_year}.")
            return redirect('ai_lab')

        if not (2014 <= end_year <= current_year):
            messages.error(request, f"End year must be between 2014 and {current_year}.")
            return redirect('ai_lab')

        if start_year > end_year:
            messages.error(request, "Start year cannot be greater than end year.")
            return redirect('ai_lab')

        # 3. Semester Validation
        if not sem:
            messages.error(request, "Please select a semester.")
            return redirect('ai_lab')

        # 4. Base Paper Query
        papers = Paper.objects.filter(
            year__range=(start_year, end_year),
            semester=sem
        )

        # 5. Apply DB Filters with those user selected paramters
        if institution and institution != 'All':
            papers = papers.filter(college__name=institution)

        if stream_id and stream_id != 'All':
            papers = papers.filter(stream_id=stream_id)

        if exam_type and exam_type != 'All':
            papers = papers.filter(exam_type=exam_type)

        # 6. Extract unique subject descriptors for the selection table
        subjects = papers.values(
            'subject_name',
            'subject_code',
            'year',
            'exam_type'
        ).distinct().order_by('-year')

        return render(request, 'ai_select_subject.html', {
            'subjects': subjects,
            'task': task,
            'filters': request.POST # request.POST behaves like a Python dictionary containing every single form input the user submitted on the previous page
        })

    return redirect('ai_lab')



# ------------ Actual AI Analyser ------------
def ai_analyze(request): # This function handles the analysis of selected papers that will be given to the AI for processing
    if request.method == 'POST':
        task = request.POST.get('task_type')
        combined_text = "" # This is IMP as we will be concatenating the text extracted from multiple PDFs into this single variable to then send it as a single payload to the AI for analysis, instead of sending multiple separate API calls for each document which would be inefficient and costly.

        # Process text based on whether data lives inside historical(Already uploaded DB tables) tables or a direct file submission
        if task in ['topics', 'summary','mock_test']:
            subject_name = request.POST.get('selected_subject') # Get the selected subject name and exam type in next line
            exam_type = request.POST.get('exam_type')
            papers = Paper.objects.filter( # Filter papers based on selected subject, year range, and semester
                subject_name=subject_name,
                year__range=(request.POST.get('start_year'), request.POST.get('end_year')),
                semester=request.POST.get('semester')
            )
            if exam_type and exam_type != 'All': # Check if a specific exam type is selected, if yes then filter by exam type also
                papers = papers.filter(exam_type=exam_type)

            # We will limit to 5 historical documents to optimize API constraints so that we don't exceed token limits.Only up to 5 papers will be processed.
            for paper in papers[:5]: # FOR NOW, This Line will actually never be utilized as On the front end, user interactions are constrained i.e. manual uploads are limited to 3 slots by the UI layout, and typical database lookups narrow down to 1 or 2 papers based on targeted year filters.
                combined_text += extract_text_from_pdf(paper.pdf_file)

        elif task == 'pdf_upload':
            # Iterate through separate multi-file input slots sequentially
            for slot in ['pdf1', 'pdf2', 'pdf3']:
                f = request.FILES.get(slot)
                if f: # if file exists
                    combined_text += extract_text_from_pdf(f) # combine extracted text from uploaded PDFs one after another

        if not combined_text.strip(): # Check if no text was extracted
            return render(request, 'ai_result.html', {'result': "Error: No text could be extracted. Please check your files or selection."})

        # The specific prompt for AI is controlled down inside 'ai_utils' based on 'task'; so get_gemini_analysis() is in ai_utils.py
        result = get_gemini_analysis(combined_text, task) # Call the analysis function with the combined text and task type

        return render(request, 'ai_result.html', {'result': result, 'task': task})

    return redirect('ai_lab')
