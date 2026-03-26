from django.shortcuts import render, redirect

def about_view(request):
    return render(request,'about_us.html')