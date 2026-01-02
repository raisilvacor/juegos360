"""
Vistas para la tienda de juegos Xbox 360
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Juego, Pedido, ItemPedido
from .mercadopago_client import MercadoPagoClient
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth import get_user_model


def index(request):
    """Vista para la página principal"""
    try:
        # Obtener juegos destacados (los más recientes disponibles)
        juegos_destacados = Juego.objects.filter(disponible=True).order_by('-fecha_creacion')[:6]
        
        # Obtener algunos juegos por género para mostrar variedad
        juegos_accion = Juego.objects.filter(disponible=True, genero='accion')[:4]
        juegos_rpg = Juego.objects.filter(disponible=True, genero='rpg')[:4]
    except Exception:
        # Si hay error (tabla no existe), retornar listas vacías
        juegos_destacados = []
        juegos_accion = []
        juegos_rpg = []
    
    context = {
        'juegos_destacados': juegos_destacados,
        'juegos_accion': juegos_accion,
        'juegos_rpg': juegos_rpg,
    }
    return render(request, 'tienda/index.html', context)


def catalogo(request):
    """Vista para el catálogo completo de juegos"""
    juegos = Juego.objects.filter(disponible=True)
    
    # Filtros
    genero = request.GET.get('genero')
    busqueda = request.GET.get('busqueda')
    orden = request.GET.get('orden', 'recientes')
    
    if genero:
        juegos = juegos.filter(genero=genero)
    
    if busqueda:
        juegos = juegos.filter(
            Q(titulo__icontains=busqueda) |
            Q(desarrolladora__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    # Ordenamiento
    if orden == 'precio_asc':
        juegos = juegos.order_by('precio')
    elif orden == 'precio_desc':
        juegos = juegos.order_by('-precio')
    elif orden == 'titulo':
        juegos = juegos.order_by('titulo')
    else:  # recientes
        juegos = juegos.order_by('-fecha_creacion')
    
    # Obtener géneros únicos para el filtro
    generos = Juego.objects.filter(disponible=True).values_list('genero', flat=True).distinct()
    generos_disponibles = [choice[0] for choice in Juego.GENEROS if choice[0] in generos]
    
    context = {
        'juegos': juegos,
        'generos_disponibles': generos_disponibles,
        'genero_actual': genero,
        'busqueda_actual': busqueda,
        'orden_actual': orden,
    }
    return render(request, 'tienda/catalogo.html', context)


def detalle_juego(request, juego_id):
    """Vista para los detalles de un juego"""
    juego = get_object_or_404(Juego, id=juego_id, disponible=True)
    
    # Obtener juegos relacionados (mismo género)
    juegos_relacionados = Juego.objects.filter(
        genero=juego.genero,
        disponible=True
    ).exclude(id=juego.id)[:4]
    
    context = {
        'juego': juego,
        'juegos_relacionados': juegos_relacionados,
    }
    return render(request, 'tienda/detalle_juego.html', context)


def agregar_al_carrito(request, juego_id):
    """Vista para agregar un juego al carrito"""
    juego = get_object_or_404(Juego, id=juego_id, disponible=True)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Inicializar carrito si no existe
        if 'carrito' not in request.session:
            request.session['carrito'] = {}
        
        # Agregar o actualizar cantidad
        carrito = request.session['carrito']
        if str(juego_id) in carrito:
            carrito[str(juego_id)] += cantidad
        else:
            carrito[str(juego_id)] = cantidad
        
        request.session['carrito'] = carrito
        messages.success(request, f'{juego.titulo} agregado al carrito')
        
        # Redirigir según el origen
        if request.POST.get('redirect') == 'carrito':
            return redirect('carrito')
        else:
            return redirect('detalle_juego', juego_id=juego_id)
    
    return redirect('detalle_juego', juego_id=juego_id)


def carrito_view(request):
    """Vista para mostrar el carrito de compras"""
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    
    for juego_id, cantidad in carrito.items():
        try:
            juego = Juego.objects.get(id=juego_id, disponible=True)
            subtotal = float(juego.precio) * cantidad
            items.append({
                'juego': juego,
                'cantidad': cantidad,
                'subtotal': subtotal,
            })
            total += subtotal
        except Juego.DoesNotExist:
            # Si el juego ya no existe o no está disponible, eliminarlo del carrito
            del carrito[juego_id]
            request.session['carrito'] = carrito
    
    context = {
        'items': items,
        'total': round(total, 2),
    }
    return render(request, 'tienda/carrito.html', context)


def actualizar_carrito(request):
    """Vista para actualizar cantidades en el carrito"""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        for juego_id, cantidad in request.POST.items():
            if juego_id.startswith('cantidad_'):
                juego_id = juego_id.replace('cantidad_', '')
                cantidad = int(cantidad)
                
                if cantidad > 0:
                    carrito[juego_id] = cantidad
                else:
                    # Eliminar del carrito si la cantidad es 0
                    if juego_id in carrito:
                        del carrito[juego_id]
        
        request.session['carrito'] = carrito
        messages.success(request, 'Carrito actualizado')
    
    return redirect('carrito')


def eliminar_del_carrito(request, juego_id):
    """Vista para eliminar un juego del carrito"""
    carrito = request.session.get('carrito', {})
    
    if str(juego_id) in carrito:
        juego = get_object_or_404(Juego, id=juego_id)
        del carrito[str(juego_id)]
        request.session['carrito'] = carrito
        messages.success(request, f'{juego.titulo} eliminado del carrito')
    
    return redirect('carrito')


def crear_pedido(request):
    """Vista para crear un pedido desde el carrito e integrar con Ualá"""
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.error(request, 'Tu carrito está vacío')
        return redirect('carrito')
    
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        email = request.POST.get('email')
        
        if not nombre_cliente or not email:
            messages.error(request, 'Por favor completa todos los campos')
            return redirect('carrito')
        
        # Calcular total
        total = 0
        items_data = []
        
        for juego_id, cantidad in carrito.items():
            try:
                juego = Juego.objects.get(id=juego_id, disponible=True)
                subtotal = float(juego.precio) * cantidad
                total += subtotal
                items_data.append({
                    'juego': juego,
                    'cantidad': cantidad,
                    'precio': float(juego.precio),
                })
            except Juego.DoesNotExist:
                continue
        
        if not items_data:
            messages.error(request, 'No hay juegos válidos en tu carrito')
            return redirect('carrito')
        
        # Crear pedido
        pedido = Pedido.objects.create(
            nombre_cliente=nombre_cliente,
            email=email,
            total=round(total, 2),
            estado='pendiente'
        )
        
        # Crear items del pedido
        items_pedido = []
        for item_data in items_data:
            item = ItemPedido.objects.create(
                pedido=pedido,
                juego=item_data['juego'],
                cantidad=item_data['cantidad'],
                precio=item_data['precio']
            )
            items_pedido.append(item)
        
        # SOLO Mercado Pago - sin fallbacks
        try:
            mp_client = MercadoPagoClient()
            
            # Crear preferencia en Mercado Pago
            preferencia = mp_client.crear_preferencia(pedido, items_pedido)
            
            # Validar que recibimos init_point
            checkout_url = preferencia.get('init_point')
            if not checkout_url:
                # Si no hay init_point, eliminar el pedido y mostrar error
                pedido.delete()
                messages.error(request, 'Error: No se recibió la URL de pago de Mercado Pago. Intenta nuevamente.')
                return redirect('carrito')
            
            # Guardar información de Mercado Pago en el pedido
            pedido.mp_preference_id = preferencia.get('id')
            pedido.mp_checkout_url = checkout_url
            pedido.mp_status = 'pending'
            pedido.save()
            
            # Limpiar carrito antes de redirigir
            request.session['carrito'] = {}
            
            # Redirigir DIRECTAMENTE al checkout de Mercado Pago
            return redirect(checkout_url)
            
        except Exception as e:
            # Si hay error, ELIMINAR el pedido y mostrar error claro
            pedido.delete()
            error_msg = str(e)
            
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error al crear preferencia Mercado Pago: {error_msg}")
            
            messages.error(
                request, 
                f'Error al procesar el pago: {error_msg}. '
                'Por favor verifica tus datos e intenta nuevamente.'
            )
            return redirect('carrito')
    
    return redirect('carrito')


def detalle_pedido(request, pedido_id):
    """Vista para mostrar los detalles de un pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Si el pedido está pendiente pero no tiene preferencia de Mercado Pago, intentar crearla
    if pedido.estado == 'pendiente' and not pedido.mp_preference_id and getattr(settings, 'MERCADOPAGO_ENABLED', True):
        try:
            mp_client = MercadoPagoClient()
            items_pedido = pedido.items.all()
            
            if items_pedido.exists():
                # Crear preferencia en Mercado Pago
                preferencia = mp_client.crear_preferencia(pedido, items_pedido)
                
                # Guardar información de Mercado Pago en el pedido
                pedido.mp_preference_id = preferencia.get('id')
                pedido.mp_checkout_url = preferencia.get('init_point')
                pedido.mp_status = 'pending'
                pedido.save()
                
                checkout_url = preferencia.get('init_point')
                if checkout_url:
                    messages.success(request, 'Preferencia de pago creada. Redirigiendo al checkout...')
                    return redirect(checkout_url)
                else:
                    raise Exception("No se recibió init_point en la respuesta")
        except Exception as e:
            # Si hay error, mostrar mensaje pero continuar
            error_msg = str(e)
            messages.warning(request, f'No se pudo crear la preferencia de pago. Error: {error_msg}')
    
    # Verificar estado del pago si hay parámetros en la URL (retorno de Mercado Pago)
    status_param = request.GET.get('status')
    if status_param and pedido.mp_preference_id:
        if status_param == 'approved':
            pedido.estado = 'pagado'
            pedido.mp_status = 'approved'
            pedido.save()
            messages.success(request, '¡Pago confirmado!')
        elif status_param == 'rejected':
            pedido.estado = 'rechazado'
            pedido.mp_status = 'rejected'
            pedido.save()
        elif status_param == 'pending':
            pedido.mp_status = 'pending'
            pedido.save()
    
    context = {
        'pedido': pedido,
    }
    return render(request, 'tienda/detalle_pedido.html', context)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def webhook_mercadopago(request):
    """
    Webhook para recibir notificaciones de Mercado Pago sobre cambios en los pagos
    """
    try:
        # Mercado Pago puede enviar datos como POST con JSON o como GET con query params
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET.dict()
        
        # Obtener información del pago
        # Mercado Pago envía 'data.id' con el ID del pago
        payment_id = data.get('data', {}).get('id') if isinstance(data.get('data'), dict) else data.get('id')
        type_notification = data.get('type', '')
        
        if not payment_id:
            return JsonResponse({'error': 'payment_id no proporcionado'}, status=400)
        
        # Obtener información del pago desde Mercado Pago
        try:
            mp_client = MercadoPagoClient()
            pago_info = mp_client.obtener_pago(payment_id)
            
            # Buscar el pedido por external_reference
            external_reference = pago_info.get('external_reference')
            if not external_reference:
                return JsonResponse({'error': 'external_reference no encontrado'}, status=400)
            
            try:
                pedido = Pedido.objects.get(id=int(external_reference))
            except (Pedido.DoesNotExist, ValueError):
                return JsonResponse({'error': 'Pedido no encontrado'}, status=404)
            
            # Actualizar estado del pedido según el pago
            status_pago = pago_info.get('status', '').lower()
            if status_pago == 'approved':
                pedido.estado = 'pagado'
                pedido.mp_status = 'approved'
                pedido.mp_payment_id = str(payment_id)
                pedido.save()
            elif status_pago == 'rejected' or status_pago == 'cancelled':
                pedido.estado = 'rechazado'
                pedido.mp_status = status_pago
                pedido.mp_payment_id = str(payment_id)
                pedido.save()
            elif status_pago == 'pending':
                pedido.mp_status = 'pending'
                pedido.mp_payment_id = str(payment_id)
                pedido.save()
            
            return JsonResponse({'status': 'ok', 'pedido_id': pedido.id})
            
        except Exception as e:
            return JsonResponse({'error': f'Error al procesar pago: {str(e)}'}, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

