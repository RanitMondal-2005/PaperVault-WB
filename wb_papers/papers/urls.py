from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.paper_search, name='papers'),
    path('upload/', views.upload_paper, name='upload'),
    path('paper/edit/<int:pk>/', views.edit_paper, name='edit_paper'),
    path('paper/delete/<int:pk>/', views.delete_paper, name='delete_paper'),
]