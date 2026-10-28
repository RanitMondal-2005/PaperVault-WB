from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Material
from .forms import MaterialUploadForm
from colleges.models import College, Stream


# ------------------ Materials Listing & Search ------------------
def materials_list(request):
    # select_related caches FK rows in a single SQL JOIN
    materials = Material.objects.select_related('college', 'stream', 'uploaded_by').all()

    # Always grab ALL distinct placement subjects from the entire database table
    placement_subjects = (
        Material.objects.filter(material_type='PLACEMENT') # Scans the Material table and selects only rows where the material_type column == 'PLACEMENT'
        .exclude(subject_name__isnull=True)
        .exclude(subject_name__exact='')
        .values_list('subject_name', flat=True)
        .distinct()
        .order_by('subject_name')
    )

    # Extract query parameters cleanly
    college_id = request.GET.get('college', '').strip()
    stream_id = request.GET.get('stream', '').strip()
    sem = request.GET.get('semester', '').strip()
    material_type = request.GET.get('material_type', '').strip()
    placement_subject = request.GET.get('placement_subject', '').strip()

    # Filter logic : EXACT ID Matching with Filter Chaining (AND)
    if college_id:
        materials = materials.filter(college_id=college_id)
    if stream_id:
        materials = materials.filter(stream_id=stream_id)
    if sem:
        materials = materials.filter(semester=sem)
    if material_type:
        materials = materials.filter(material_type=material_type)
    if placement_subject:
        materials = materials.filter(subject_name=placement_subject)

    # 10 materials per page : Pagination
    paginator = Paginator(materials, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'materials': page_obj,
        'colleges': College.objects.all(),
        'streams': Stream.objects.all(),
        'placement_subjects': placement_subjects, # Populates the dropdown of all present Subjects when PLACEMENT selected
    }
    return render(request, 'materials.html', context)


# ------------------ Upload Material ------------------
@login_required
def upload_material(request):
    # Guard: ensure profile exists
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Account error: Profile not found.")
        return redirect('dashboard')

    # RBAC: Only verified faculty can upload materials
    if request.user.profile.role != 'FACULTY' or not request.user.profile.is_verified:
        messages.warning(request, "Verification Pending: Access Denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False lets us bind uploaded_by before inserting & Saving into DB
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            messages.success(request, "Material successfully uploaded!")
            return redirect('materials')
        else:
            messages.error(request, "Error uploading material. Please check the form.")
    else:
        form = MaterialUploadForm()

    return render(request, 'upload_material.html', {'form': form})


# ------------------ Edit Material ------------------
@login_required
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    # Security check: only creator can edit
    if material.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot edit this material.")
        return redirect('materials')

    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES, instance=material)
        # If user is not replacing the PDF, keep the existing one optional
        if not request.FILES.get('pdf_file'):
            form.fields['pdf_file'].required = False

        if form.is_valid():
            form.save()
            messages.success(request, "Material updated successfully!")
            return redirect('materials')
        else:
            messages.error(request, "Please fix the highlighted errors.")
    else:
        form = MaterialUploadForm(instance=material)
        form.fields['pdf_file'].required = False

    return render(request, 'edit_material.html', {'form': form, 'material': material})


# ------------------ Delete Material ------------------
@login_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    # Security check: only creator can delete
    if material.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot delete this material.")
        return redirect('materials')

    if request.method == 'POST':
        material.delete()
        messages.success(request, "Material has been permanently removed.")
        return redirect('materials')

    return render(request, 'delete_material.html', {'material': material})

