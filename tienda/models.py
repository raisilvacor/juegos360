"""
Modelos para la tienda de juegos Xbox 360
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Juego(models.Model):
    """Modelo que representa un juego de Xbox 360"""
    
    # Géneros disponibles
    GENEROS = [
        ('accion', 'Acción'),
        ('aventura', 'Aventura'),
        ('rpg', 'RPG'),
        ('deportes', 'Deportes'),
        ('carreras', 'Carreras'),
        ('estrategia', 'Estrategia'),
        ('shooter', 'Shooter'),
        ('lucha', 'Lucha'),
        ('plataformas', 'Plataformas'),
        ('terror', 'Terror'),
    ]
    
    # Clasificaciones indicativas
    CLASIFICACIONES = [
        ('E', 'E - Everyone (Todos)'),
        ('E10+', 'E10+ - Everyone 10+ (Todos +10)'),
        ('T', 'T - Teen (Adolescentes)'),
        ('M', 'M - Mature (Maduro)'),
        ('AO', 'AO - Adults Only (Solo Adultos)'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    genero = models.CharField(max_length=50, choices=GENEROS, verbose_name='Género')
    desarrolladora = models.CharField(max_length=200, verbose_name='Desarrolladora')
    ano_lanzamiento = models.IntegerField(
        verbose_name='Año de Lanzamiento',
        validators=[MinValueValidator(2005), MaxValueValidator(2016)]
    )
    clasificacion = models.CharField(
        max_length=10,
        choices=CLASIFICACIONES,
        verbose_name='Clasificación Indicativa'
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio',
        validators=[MinValueValidator(0)]
    )
    imagen = models.URLField(
        max_length=500,
        verbose_name='URL de Imagen de Portada',
        blank=True,
        null=True,
        help_text='URL completa de la imagen del juego (ejemplo: https://ejemplo.com/imagen.jpg)'
    )
    link_descarga = models.URLField(
        max_length=500,
        verbose_name='Link de Descarga',
        blank=True,
        null=True,
        help_text='URL del link de descarga del juego. Se mostrará al cliente después del pago confirmado.'
    )
    disponible = models.BooleanField(default=True, verbose_name='Disponible')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')
    
    class Meta:
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo


class Pedido(models.Model):
    """Modelo que representa un pedido"""
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('pagado', 'Pagado'),
        ('rechazado', 'Rechazado'),
    ]
    
    nombre_cliente = models.CharField(max_length=200, verbose_name='Nombre del Cliente')
    email = models.EmailField(verbose_name='Email')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    # Campos para integración con Mercado Pago
    mp_preference_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='ID Preferencia Mercado Pago')
    mp_checkout_url = models.URLField(blank=True, null=True, verbose_name='URL Checkout Mercado Pago')
    mp_status = models.CharField(max_length=50, blank=True, null=True, verbose_name='Estado Mercado Pago')
    mp_payment_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='ID Pago Mercado Pago')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'Pedido #{self.id} - {self.nombre_cliente}'


class ItemPedido(models.Model):
    """Modelo que representa un item dentro de un pedido"""
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, verbose_name='Juego')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        return f'{self.cantidad}x {self.juego.titulo}'
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.cantidad * self.precio

