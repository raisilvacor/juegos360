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
from django.core.management import call_command
from io import StringIO
import json
import sys
from .models import Juego, Pedido, ItemPedido
from .mercadopago_client import MercadoPagoClient
from django.contrib.auth import get_user_model

User = get_user_model()


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
    
    # Aplicar filtros
    if genero:
        juegos = juegos.filter(genero=genero)
    
    if busqueda:
        juegos = juegos.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(desarrolladora__icontains=busqueda)
        )
    
    # Ordenar
    if orden == 'precio_asc':
        juegos = juegos.order_by('precio')
    elif orden == 'precio_desc':
        juegos = juegos.order_by('-precio')
    elif orden == 'titulo':
        juegos = juegos.order_by('titulo')
    else:  # recientes
        juegos = juegos.order_by('-fecha_creacion')
    
    # Obtener géneros disponibles para el filtro
    generos_disponibles = Juego.objects.filter(disponible=True).values_list('genero', flat=True).distinct()
    
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
    
    # Obtener juegos relacionados (mismo género, excluyendo el actual)
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
    if request.method == 'POST':
        juego = get_object_or_404(Juego, id=juego_id, disponible=True)
        cantidad = int(request.POST.get('cantidad', 1))
        
        if cantidad < 1:
            cantidad = 1
        
        # Obtener o inicializar el carrito en la sesión
        carrito = request.session.get('carrito', {})
        
        # Agregar o actualizar la cantidad del juego
        if str(juego_id) in carrito:
            carrito[str(juego_id)] += cantidad
        else:
            carrito[str(juego_id)] = cantidad
        
        request.session['carrito'] = carrito
        messages.success(request, f'{juego.titulo} agregado al carrito.')
    
    return redirect('detalle_juego', juego_id=juego_id)


def actualizar_carrito(request):
    """Vista para actualizar las cantidades del carrito"""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        for juego_id, cantidad in request.POST.items():
            if juego_id.startswith('cantidad_'):
                juego_id = juego_id.replace('cantidad_', '')
                cantidad = int(cantidad)
                
                if cantidad > 0:
                    carrito[juego_id] = cantidad
                elif juego_id in carrito:
                    del carrito[juego_id]
        
        request.session['carrito'] = carrito
        messages.success(request, 'Carrito actualizado.')
    
    return redirect('carrito')


def eliminar_del_carrito(request, juego_id):
    """Vista para eliminar un juego del carrito"""
    carrito = request.session.get('carrito', {})
    
    if str(juego_id) in carrito:
        del carrito[str(juego_id)]
        request.session['carrito'] = carrito
        messages.success(request, 'Juego eliminado del carrito.')
    
    return redirect('carrito')


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
                'subtotal': subtotal
            })
            total += subtotal
        except Juego.DoesNotExist:
            # Si el juego no existe, eliminarlo del carrito
            del carrito[juego_id]
            request.session['carrito'] = carrito
    
    context = {
        'items': items,
        'total': round(total, 2),
    }
    return render(request, 'tienda/carrito.html', context)


def crear_pedido(request):
    """Vista para crear un pedido desde el carrito"""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        if not carrito:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('carrito')
        
        # Obtener datos del formulario
        nombre_cliente = request.POST.get('nombre_cliente', '').strip()
        email = request.POST.get('email', '').strip()
        
        if not nombre_cliente or not email:
            messages.error(request, 'Por favor completa todos los campos.')
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
                    'precio': juego.precio
                })
            except Juego.DoesNotExist:
                continue
        
        if not items_data:
            messages.error(request, 'No hay juegos válidos en tu carrito.')
            return redirect('carrito')
        
        # Crear el pedido
        pedido = Pedido.objects.create(
            nombre_cliente=nombre_cliente,
            email=email,
            total=round(total, 2),
            estado='pendiente'
        )
        
        # Crear los items del pedido
        for item_data in items_data:
            ItemPedido.objects.create(
                pedido=pedido,
                juego=item_data['juego'],
                cantidad=item_data['cantidad'],
                precio=item_data['precio']
            )
        
        # Crear preferencia de Mercado Pago
        try:
            mp_client = MercadoPagoClient()
            items_mp = ItemPedido.objects.filter(pedido=pedido)
            
            preferencia = mp_client.crear_preferencia(pedido, items_mp)
            
            if preferencia and 'init_point' in preferencia:
                pedido.mp_preference_id = preferencia.get('id')
                pedido.mp_checkout_url = preferencia.get('init_point')
                pedido.save()
                
                # Limpiar el carrito
                request.session['carrito'] = {}
                
                return redirect('detalle_pedido', pedido_id=pedido.id)
            else:
                # Si falla la creación de la preferencia, eliminar el pedido
                pedido.delete()
                messages.error(request, 'No se pudo crear la preferencia de pago. Por favor intenta más tarde.')
                return redirect('carrito')
        
        except Exception as e:
            # Si hay error, eliminar el pedido
            pedido.delete()
            messages.error(request, f'Error al procesar el pago: {str(e)}. Por favor verifica tus datos e intenta nuevamente.')
            return redirect('carrito')
    
    return redirect('carrito')


def detalle_pedido(request, pedido_id):
    """Vista para mostrar los detalles de un pedido"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Verificar estado del pago en Mercado Pago si está pendiente
    if pedido.estado == 'pendiente' and pedido.mp_preference_id:
        try:
            mp_client = MercadoPagoClient()
            status = request.GET.get('status')
            
            if status:
                # Actualizar estado según el parámetro de la URL
                if status == 'approved':
                    pedido.estado = 'pagado'
                    pedido.mp_status = 'approved'
                    pedido.save()
                elif status == 'rejected':
                    pedido.estado = 'rechazado'
                    pedido.mp_status = 'rejected'
                    pedido.save()
                elif status == 'pending':
                    pedido.mp_status = 'pending'
                    pedido.save()
        except Exception:
            pass
    
    context = {
        'pedido': pedido,
    }
    return render(request, 'tienda/detalle_pedido.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def webhook_mercadopago(request):
    """
    Webhook para recibir notificaciones de Mercado Pago
    """
    try:
        data = json.loads(request.body)
        payment_id = data.get('data', {}).get('id')
        
        if not payment_id:
            return JsonResponse({'status': 'error', 'message': 'No payment ID'}, status=400)
        
        # Obtener información del pago
        mp_client = MercadoPagoClient()
        payment_info = mp_client.obtener_pago(payment_id)
        
        if payment_info:
            external_reference = payment_info.get('external_reference')
            
            if external_reference:
                try:
                    pedido = Pedido.objects.get(id=int(external_reference))
                    
                    # Actualizar estado del pedido
                    status = payment_info.get('status')
                    if status == 'approved':
                        pedido.estado = 'pagado'
                        pedido.mp_status = 'approved'
                        pedido.mp_payment_id = payment_id
                        pedido.save()
                    elif status == 'rejected':
                        pedido.estado = 'rechazado'
                        pedido.mp_status = 'rejected'
                        pedido.save()
                    elif status == 'pending':
                        pedido.mp_status = 'pending'
                        pedido.save()
                    
                    return JsonResponse({'status': 'ok'})
                except Pedido.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid payment info'}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def crear_admin_view(request):
    """
    Vista temporária para criar superusuário via URL
    Acesse: https://juegos360.onrender.com/criar-admin/
    """
    User = get_user_model()
    
    # Verificar se já existe um superusuário
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("""
        <html>
        <head><title>Admin já existe</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>⚠️ Superusuário já existe!</h1>
            <p>Já existe um superusuário no sistema.</p>
            <p><a href="/admin/">Acessar Admin</a></p>
        </body>
        </html>
        """)
    
    # Criar superusuário
    try:
        username = 'admin'
        email = 'admin@juegos360.com'
        password = 'admin123'
        
        User.objects.create_superuser(username, email, password)
        
        return HttpResponse(f"""
        <html>
        <head><title>Admin Criado</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>✅ Superusuário criado com sucesso!</h1>
            <div style="background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px;">
                <p><strong>Usuário:</strong> {username}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Senha:</strong> {password}</p>
            </div>
            <p style="color: red;"><strong>⚠️ IMPORTANTE:</strong> Altere a senha após o primeiro acesso!</p>
            <p><a href="/admin/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Acessar Admin</a></p>
            <p style="margin-top: 30px; color: #666; font-size: 12px;">Após criar o admin, remova esta rota por segurança.</p>
        </body>
        </html>
        """)
    except Exception as e:
        return HttpResponse(f"Error al crear superusuario: {str(e)}", status=500)


@csrf_exempt
def importar_juegos_view(request):
    """
    Vista temporária para importar juegos del índice via URL
    Acesse: https://juegos360.onrender.com/importar-juegos/
    """
    
    # Verificar token de seguridad (opcional, puede configurarse en variables de entorno)
    token = request.GET.get('token', '')
    expected_token = getattr(settings, 'IMPORT_TOKEN', 'importar123')
    
    if token != expected_token:
        return HttpResponse("""
        <html>
        <head><title>Importar Juegos</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>Importar Juegos del Índice</h1>
            <p>Esta página importa todos los juegos del índice con precio de 3000 pesos.</p>
            <p style="color: red;"><strong>⚠️ ADVERTENCIA:</strong> Esta acción puede tardar varios minutos.</p>
            <p><a href="?token=importar123" style="background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 18px;">Importar Juegos Ahora</a></p>
            <p style="margin-top: 30px; color: #666; font-size: 12px;">Después de importar, elimine esta ruta por seguridad.</p>
        </body>
        </html>
        """)
    
    # Ejecutar el comando de importación
    try:
        # Capturar la salida del comando
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        call_command('importar_juegos_indice')
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Contar juegos después de la importación
        total = Juego.objects.count()
        disponibles = Juego.objects.filter(disponible=True).count()
        con_precio_3000 = Juego.objects.filter(precio=3000).count()
        
        return HttpResponse(f"""
        <html>
        <head><title>Juegos Importados</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1 style="color: #28a745;">✅ ¡Juegos Importados con Éxito!</h1>
            <div style="background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px; text-align: left; max-width: 600px; margin-left: auto; margin-right: auto;">
                <h3>Estadísticas:</h3>
                <ul>
                    <li><strong>Total de juegos:</strong> {total}</li>
                    <li><strong>Juegos disponibles:</strong> {disponibles}</li>
                    <li><strong>Juegos con precio 3000:</strong> {con_precio_3000}</li>
                </ul>
            </div>
            <div style="background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; max-width: 600px; margin-left: auto; margin-right: auto;">
                <p style="color: #856404;"><strong>⚠️ IMPORTANTE:</strong> Elimine esta ruta después de usar por seguridad.</p>
            </div>
            <p><a href="/admin/tienda/juego/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Ver Juegos en el Admin</a></p>
            <p><a href="/catalogo/" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-left: 10px;">Ver Catálogo Público</a></p>
            <details style="margin-top: 30px; text-align: left; max-width: 800px; margin-left: auto; margin-right: auto;">
                <summary style="cursor: pointer; color: #666;">Ver detalles de la importación</summary>
                <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;">{output[:2000]}</pre>
            </details>
        </body>
        </html>
        """)
    except Exception as e:
        sys.stdout = old_stdout
        return HttpResponse(f"""
        <html>
        <head><title>Error al Importar</title></head>
        <body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1 style="color: red;">❌ Error al Importar Juegos</h1>
            <p style="color: red;">{str(e)}</p>
            <p><a href="/admin/">Volver al Admin</a></p>
        </body>
        </html>
        """, status=500)


def robots_txt(request):
    """Vista para servir robots.txt"""
    from django.conf import settings
    from django.http import HttpResponse
    import os
    
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    
    if os.path.exists(robots_path):
        with open(robots_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    else:
        # Fallback se o arquivo não existir
        content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://juegos360.onrender.com/sitemap.xml
"""
        return HttpResponse(content, content_type='text/plain')
