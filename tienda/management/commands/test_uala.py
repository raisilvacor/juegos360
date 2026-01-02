"""
Comando para probar la conexión con Ualá Bis
"""
from django.core.management.base import BaseCommand
from tienda.uala_client import UalaClient
import requests


class Command(BaseCommand):
    help = 'Prueba la conexión y autenticación con Ualá Bis'

    def add_arguments(self, parser):
        parser.add_argument(
            '--production',
            action='store_true',
            help='Usar credenciales de producción en lugar de stage',
        )

    def handle(self, *args, **options):
        from django.conf import settings
        
        # Configurar temporalmente si se solicita producción
        if options['production']:
            settings.UALA_PRODUCTION = True
            env = "PRODUCCIÓN"
        else:
            settings.UALA_PRODUCTION = False
            env = "STAGE"
        
        self.stdout.write(f'\n{"="*60}')
        self.stdout.write(f'Probando conexión con Ualá Bis - {env}')
        self.stdout.write(f'{"="*60}\n')
        
        try:
            client = UalaClient()
            
            self.stdout.write(f'Base URL: {client.base_url}')
            self.stdout.write(f'Username: {client.username}')
            self.stdout.write(f'Client ID: {client.client_id[:20]}...')
            self.stdout.write(f'Client Secret: {"*" * 20}...\n')
            
            self.stdout.write('Intentando obtener token...')
            
            # Intentar obtener token
            token = client._get_token()
            
            if token:
                self.stdout.write(
                    self.style.SUCCESS(f'\n✓ Token obtenido exitosamente!')
                )
                self.stdout.write(f'Token: {token[:50]}...\n')
                
                # Probar crear una orden de prueba
                self.stdout.write('Probando creación de orden de prueba...')
                try:
                    from tienda.models import Pedido, Juego, ItemPedido
                    
                    # Buscar un pedido existente o crear uno de prueba
                    pedido = Pedido.objects.filter(estado='pendiente').first()
                    
                    if not pedido:
                        self.stdout.write(self.style.WARNING(
                            'No hay pedidos pendientes. Creando pedido de prueba...'
                        ))
                        # Crear pedido de prueba
                        pedido = Pedido.objects.create(
                            nombre_cliente='Test User',
                            email='test@example.com',
                            total=100.00,
                            estado='pendiente'
                        )
                        
                        # Agregar un juego de prueba si existe
                        juego = Juego.objects.first()
                        if juego:
                            ItemPedido.objects.create(
                                pedido=pedido,
                                juego=juego,
                                cantidad=1,
                                precio=100.00
                            )
                    
                    items = pedido.items.all()
                    if items.exists():
                        orden = client.crear_orden(pedido, items)
                        self.stdout.write(
                            self.style.SUCCESS(f'\n✓ Orden creada exitosamente!')
                        )
                        self.stdout.write(f'Order ID: {orden.get("id")}')
                        self.stdout.write(f'Checkout URL: {orden.get("checkout_url")}')
                    else:
                        self.stdout.write(self.style.WARNING(
                            'El pedido no tiene items. No se puede crear orden de prueba.'
                        ))
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'\n✗ Error al crear orden: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR('\n✗ No se pudo obtener el token')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n✗ Error: {str(e)}')
            )
            self.stdout.write('\nPosibles causas:')
            self.stdout.write('1. Las credenciales son incorrectas')
            self.stdout.write('2. Las credenciales han expirado')
            self.stdout.write('3. El usuario no tiene permisos')
            self.stdout.write('4. Problemas de conectividad')
            self.stdout.write('\nSugerencias:')
            self.stdout.write('- Verifica las credenciales en settings.py')
            self.stdout.write('- Contacta con soporte de Ualá Bis')
            self.stdout.write('- Prueba con credenciales de producción usando --production')

