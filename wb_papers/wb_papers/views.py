from django.shortcuts import render, redirect
from django.contrib import messages

def about_view(request):
    return render(request,'about_us.html')

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_body = request.POST.get('message', '').strip()

        if not name or not email or not message_body:
            messages.error(request, "Please fill in all fields before submitting.")
            return render(request, 'contact_us.html')

        # Form is valid — show success
        # To send real emails later, configure EMAIL_BACKEND in settings.py
        # For Now Only the Illusion Logic
        messages.success(request, "Thank you for reaching out! We'll get back to you within 24-48 hours.")
        return redirect('dashboard')

    return render(request, 'contact_us.html')