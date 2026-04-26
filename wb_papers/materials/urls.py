from django.urls import path
from . import views

urlpatterns = [
    path('', views.materials_list, name='materials'),
    path('upload/', views.upload_material, name='upload_material'),
    path('edit/<int:pk>/', views.edit_material, name='edit_material'),
    path('delete/<int:pk>/', views.delete_material, name='delete_material'),
]