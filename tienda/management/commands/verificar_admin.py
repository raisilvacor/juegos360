"""
Comando para verificar se los juegos aparecen correctamente en el admin
"""
from django.core.management.base import BaseCommand
from tienda.models import Juego


class Command(BaseCommand):
    help = 'Verifica que todos los juegos estén disponibles y con precio correcto'

    def handle(self, *args, **options):
        total = Juego.objects.count()
        disponibles = Juego.objects.filter(disponible=True).count()
        con_precio_3000 = Juego.objects.filter(precio=3000).count()
        
        self.stdout.write(f'Total de juegos: {total}')
        self.stdout.write(f'Juegos disponibles: {disponibles}')
        self.stdout.write(f'Juegos con precio 3000: {con_precio_3000}')
        
        # Verificar que todos estén disponibles
        if disponibles < total:
            self.stdout.write(
                self.style.WARNING(f'ADVERTENCIA: {total - disponibles} juegos NO están disponibles')
            )
            # Hacer disponibles todos
            Juego.objects.filter(disponible=False).update(disponible=True)
            self.stdout.write(self.style.SUCCESS('Todos los juegos ahora están disponibles'))
        
        # Verificar precios
        if con_precio_3000 < total:
            self.stdout.write(
                self.style.WARNING(f'ADVERTENCIA: {total - con_precio_3000} juegos NO tienen precio 3000')
            )
            from decimal import Decimal
            Juego.objects.exclude(precio=3000).update(precio=Decimal('3000.00'))
            self.stdout.write(self.style.SUCCESS('Todos los juegos ahora tienen precio 3000'))
        
        # Mostrar algunos ejemplos
        self.stdout.write('\nPrimeros 5 juegos (más recientes):')
        for juego in Juego.objects.order_by('-fecha_creacion')[:5]:
            self.stdout.write(
                f'  - {juego.titulo} (ID: {juego.id}) - Precio: ${juego.precio} - Disponible: {juego.disponible}'
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n¡Verificación completa! Todos los juegos deberían aparecer en el admin.')
        )
        self.stdout.write('\nSi no ves los juegos en el admin:')
        self.stdout.write('  1. Recarga la página con Ctrl+F5 (o Cmd+Shift+R en Mac)')
        self.stdout.write('  2. Verifica que no haya filtros activos en el panel derecho')
        self.stdout.write('  3. Limpia el campo de búsqueda')
        self.stdout.write('  4. Verifica la paginación en la parte inferior')

