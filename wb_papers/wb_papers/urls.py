from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
   
    path('admin/', admin.site.urls), 
    path('', include('papers.urls')),
    path('users/', include('users.urls')),
    # about us page
    path('about/', views.about_view, name='about'),
    # contact us page
    path('contactUs/', views.contact_us, name='contact_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)