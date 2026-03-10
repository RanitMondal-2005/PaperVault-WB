from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.paper_search, name='papers'),
    path('upload/', views.upload_paper, name='upload'),
]