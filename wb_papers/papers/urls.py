from django.urls import path
from . import views

urlpatterns = [
    # Dashboard For all Users
    path('', views.dashboard, name='dashboard'),
    # Papers
    path('search/', views.paper_search, name='papers'),
    path('upload/', views.upload_paper, name='upload'),
    path('paper/edit/<int:pk>/', views.edit_paper, name='edit_paper'),
    path('paper/delete/<int:pk>/', views.delete_paper, name='delete_paper'),
    # Password Change for Users
    path('password-change/', views.change_password, name='password_change'),
    # AI Analyzer
    path('ai-analyzer/', views.ai_analyzer, name='ai_analyzer'),
    path('ai-lab/', views.ai_lab_dashboard, name='ai_lab'),
    path('ai-lab/select-subject/', views.ai_select_subject, name='ai_select_subject'),
    path('ai-lab/analyze/', views.ai_analyze, name='ai_analyze'),

]
