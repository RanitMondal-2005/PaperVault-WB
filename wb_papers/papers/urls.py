from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.paper_search, name='papers'),
    path('upload/', views.upload_paper, name='upload'),
    path('paper/edit/<int:pk>/', views.edit_paper, name='edit_paper'),
    path('paper/delete/<int:pk>/', views.delete_paper, name='delete_paper'),
    path('password-change/', views.change_password, name='password_change'),
    # AI Analyzer - Logic
    path('ai-lab/', views.ai_lab_dashboard, name='ai_lab'),
    path('ai-lab/select-subject/', views.ai_select_subject, name='ai_select_subject'),
    path('ai-lab/analyze/', views.ai_analyze, name='ai_analyze'),
]