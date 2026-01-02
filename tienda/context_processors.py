"""
Context processors para la tienda
"""
from django.db import connection


def carrito(request):
    """
    Context processor que agrega información del carrito a todos los templates
    """
    try:
        # Verificar si las tablas existen
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tienda_juego'")
            table_exists = cursor.fetchone()
        
        if not table_exists:
            return {
                'carrito_items': 0,
                'carrito_total': 0,
            }
        
        from .models import Juego
        
        carrito = request.session.get('carrito', {})
        total_items = sum(carrito.values()) if carrito else 0
        total_precio = 0
        
        # Calcular el total del precio
        for juego_id, cantidad in carrito.items():
            try:
                juego = Juego.objects.get(id=juego_id, disponible=True)
                total_precio += float(juego.precio) * cantidad
            except (Juego.DoesNotExist, Exception):
                pass
    except Exception:
        # Si hay cualquier error, retornar valores por defecto
        return {
            'carrito_items': 0,
            'carrito_total': 0,
        }
    
    return {
        'carrito_items': total_items,
        'carrito_total': round(total_precio, 2),
    }

