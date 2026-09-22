from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Registration Form
    path('register/', views.register_view, name='register'),
    # Login - Log out Logic
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Django's built-in LoginView class we just tell it to use our custom login.html template instead of Django's default ugly one. Django handles everything internally — form validation, password checking,redirect after login.
    path('logout/', views.logout_view, name='logout'),
]
