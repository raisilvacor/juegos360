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
# Em produção com Cloudinary, as imagens são servidas automaticamente
# Em desenvolvimento ou sem Cloudinary, servir arquivos locais via WhiteNoise ou static
from django.conf.urls.static import static

# Se não estiver usando Cloudinary, servir arquivos de media
if not getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME', ''):
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

