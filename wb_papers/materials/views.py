from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Material
from .forms import MaterialUploadForm
from colleges.models import College, Stream
from django.http import JsonResponse

def materials_list(request):
    materials = Material.objects.all().order_by('-uploaded_at')

    college_id = request.GET.get('college')
    stream_id = request.GET.get('stream')
    sem = request.GET.get('semester')
    material_type = request.GET.get('material_type')

    if college_id and college_id.strip():
        materials = materials.filter(college_id=college_id)
    if stream_id and stream_id.strip():
        materials = materials.filter(stream_id=stream_id)
    if sem and sem.strip():
        materials = materials.filter(semester=sem)
    if material_type and material_type.strip():
        materials = materials.filter(material_type=material_type)

    # Placement specific subject filter
    placement_subject = request.GET.get('placement_subject', '').strip()
    if placement_subject:
        materials = materials.filter(subject_name=placement_subject)

    paginator = Paginator(materials, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'materials': page_obj,
        'colleges': College.objects.all(),
        'streams': Stream.objects.all(),
    }
    return render(request, 'materials.html', context)


@login_required
def upload_material(request):
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Account error: Profile not found.")
        return redirect('dashboard')

    if request.user.profile.role == 'FACULTY' and request.user.profile.is_verified:
        if request.method == 'POST':
            form = MaterialUploadForm(request.POST, request.FILES)
            if form.is_valid():
                material = form.save(commit=False)
                material.uploaded_by = request.user
                # convert empty semester to None for placement notes
                if not material.semester:
                    material.semester = None
                material.save()
                messages.success(request, "Material successfully uploaded!")
                return redirect('materials')
            else:
                messages.error(request, "Error uploading material. Please check the form.")
        else:
            form = MaterialUploadForm()
        return render(request, 'upload_material.html', {'form': form})
    else:
        messages.warning(request, "Verification Pending: Access Denied.")
        return redirect('dashboard')


@login_required
def edit_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if material.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot edit this material.")
        return redirect('materials')

    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES, instance=material)
        if not request.FILES.get('pdf_file'):
            form.fields['pdf_file'].required = False
        if form.is_valid():
            material = form.save(commit=False)
            if not material.semester:
                material.semester = None
            material.save()
            messages.success(request, f"Material updated successfully!")
            return redirect('materials')
    else:
        form = MaterialUploadForm(instance=material)
        form.fields['pdf_file'].required = False

    return render(request, 'edit_material.html', {'form': form, 'material': material})

@login_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if material.uploaded_by != request.user:
        messages.error(request, "Access Denied: You cannot delete this material.")
        return redirect('materials')

    if request.method == 'POST':
        material.delete()
        messages.success(request, "Material has been permanently removed.")
        return redirect('materials')

    return render(request, 'delete_material.html', {'material': material})


def get_placement_subjects(request):
    """Returns distinct subjects that have PLACEMENT type materials"""
    subjects = Material.objects.filter(
        material_type='PLACEMENT'
    ).values_list('subject_name', flat=True).distinct().order_by('subject_name')
    return JsonResponse({'subjects': list(subjects)})


def get_placement_colleges(request):
    """Returns colleges that have PLACEMENT materials for a given subject"""
    subject = request.GET.get('subject', '')
    colleges = Material.objects.filter(
        material_type='PLACEMENT',
        subject_name=subject
    ).values('college__id', 'college__name').distinct()
    return JsonResponse({'colleges': list(colleges)})