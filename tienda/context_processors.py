"""
Context processors para la tienda
"""
from django.shortcuts import get_object_or_404
from .models import Juego


def carrito(request):
    """
    Context processor que agrega información del carrito a todos los templates
    """
    try:
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
        # Si hay cualquier error (tabla no existe, etc), retornar valores por defecto
        carrito = {}
        total_items = 0
        total_precio = 0
    
    return {
        'carrito_items': total_items,
        'carrito_total': round(total_precio, 2),
    }

