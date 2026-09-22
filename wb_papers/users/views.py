from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Profile

# ---------- FACULTY REGISTRATION FORM LOGIC -----------------
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 1. Save credentials to Django's Default User Table
            user = form.save()

            # 2. Create the linked Profile row directly here
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'FACULTY', # FACULTY role Hardcoded when form submitted...
                    'is_verified': False, # Starts pending admin approval...
                    'college': None,
                }
            )
            # 3. Inform user and direct them
            messages.info(
                request,
                "Registration submitted. Your account is pending verification by an administrator. Please Wait."
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm() # Create an empty form instance for GET requests i.e. when a user first visits the registration page
    return render(request, 'registration.html', {'form': form})


# --------- LogOut View : Using Django's Default Logout Function ---------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/')

# LogIn View : We used Django's built-in LoginView Class with a custom template. We could have written a custom view but Django's built-in handles all edge cases and logic properly.
