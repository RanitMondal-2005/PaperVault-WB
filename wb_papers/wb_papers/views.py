from django.shortcuts import render, redirect
from django.contrib import messages

def about_view(request):
    return render(request,'about_us.html')

def contact_us(request):
    if request.method == "POST":
        # The "Illusion" Logic: 
        # We pretend to process the data, then trigger the success message.
        messages.success(request, "Success! Your inquiry has been submitted. Our team will review your request and get back to you within 24-48 business hours. Thank you for your patience!")
        return redirect('dashboard') # This reloads the page to show the alert
    
    return render(request,'contact_us.html')