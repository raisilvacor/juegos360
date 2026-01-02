"""
Context processors para la tienda
"""
from django.shortcuts import get_object_or_404
from .models import Juego


def carrito(request):
    """
    Context processor que agrega información del carrito a todos los templates
    """
    carrito = request.session.get('carrito', {})
    total_items = sum(carrito.values())
    total_precio = 0
    
    # Calcular el total del precio
    for juego_id, cantidad in carrito.items():
        try:
            juego = Juego.objects.get(id=juego_id, disponible=True)
            total_precio += float(juego.precio) * cantidad
        except Juego.DoesNotExist:
            pass
    
    return {
        'carrito_items': total_items,
        'carrito_total': round(total_precio, 2),
    }

