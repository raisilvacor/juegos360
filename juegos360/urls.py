"""
URL configuration for juegos360 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls')),
]

# Servir archivos de media
# Sempre servir arquivos de media (WhiteNoise ou static do Django)
if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
