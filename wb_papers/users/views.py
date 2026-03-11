from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role', 'STUDENT')
            
            # Logic: Students verified by default, Faculty needs Admin check
            is_verified = True if role == 'STUDENT' else False
            
            Profile.objects.create(
                user=user,
                role=role,
                is_verified=is_verified
            )
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})