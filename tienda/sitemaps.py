"""
Sitemap para SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Juego


class JuegoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Juego.objects.filter(disponible=True)
    
    def location(self, obj):
        from django.urls import reverse
        return reverse('detalle_juego', args=[obj.id])
    
    def lastmod(self, obj):
        return obj.fecha_actualizacion


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    
    def items(self):
        return ['index', 'catalogo']
    
    def location(self, item):
        return reverse(item)

