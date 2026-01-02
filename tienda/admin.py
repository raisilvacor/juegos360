"""
Configuración del Django Admin para la tienda
"""
from django.contrib import admin
from .models import Juego, Pedido, ItemPedido


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Juego"""
    list_display = ('titulo', 'genero', 'desarrolladora', 'precio', 'disponible', 'fecha_creacion')
    list_filter = ('genero', 'clasificacion', 'disponible', 'ano_lanzamiento')
    search_fields = ('titulo', 'desarrolladora', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'imagen'),
            'description': 'Ingrese la URL completa de la imagen del juego (ejemplo: https://ejemplo.com/imagen.jpg)'
        }),
        ('Detalles del Juego', {
            'fields': ('genero', 'desarrolladora', 'ano_lanzamiento', 'clasificacion')
        }),
        ('Venta', {
            'fields': ('precio', 'disponible')
        }),
        ('Descarga', {
            'fields': ('link_descarga',),
            'description': 'Link de descarga que se mostrará al cliente después del pago confirmado.'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class ItemPedidoInline(admin.TabularInline):
    """Inline para los items del pedido"""
    model = ItemPedido
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Configuración del admin para el modelo Pedido"""
    list_display = ('id', 'nombre_cliente', 'email', 'total', 'estado', 'mp_status', 'fecha_creacion')
    list_filter = ('estado', 'mp_status', 'fecha_creacion')
    search_fields = ('nombre_cliente', 'email', 'mp_preference_id')
    readonly_fields = ('fecha_creacion', 'mp_preference_id', 'mp_checkout_url', 'mp_status', 'mp_payment_id')
    inlines = [ItemPedidoInline]
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre_cliente', 'email')
        }),
        ('Pedido', {
            'fields': ('total', 'estado', 'fecha_creacion')
        }),
        ('Información Mercado Pago', {
            'fields': ('mp_preference_id', 'mp_checkout_url', 'mp_status', 'mp_payment_id'),
            'classes': ('collapse',)
        }),
    )

