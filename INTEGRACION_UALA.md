# Integración con Ualá Bis - Juegos360

Esta documentación explica cómo funciona la integración con Ualá Bis para procesar pagos en la tienda de juegos Xbox 360.

## 📋 Configuración

### Credenciales

Las credenciales están configuradas en `juegos360/settings.py`. Por defecto, el sistema está configurado para usar el entorno **STAGE** (pruebas).

#### Cambiar a Producción

Para usar credenciales productivas, edita `juegos360/settings.py`:

```python
UALA_PRODUCTION = True  # Cambiar a True para producción
```

### Variables de Entorno (Opcional)

También puedes configurar las credenciales usando variables de entorno:

```bash
# Producción
export UALA_USERNAME="raisilva.smt"
export UALA_CLIENT_ID="eqbz8x1nFczDlKA6bVjRM86gy0BMUvrw"
export UALA_CLIENT_SECRET="Sowk0d0fzHe1F-LmuOxj6RBSDk6y7zrdHxBq74sg_knMqCNLplMDxgECf1Ieq_sX"

# Stage (pruebas)
export UALA_STAGE_USERNAME="new_user_1631906477"
export UALA_STAGE_CLIENT_ID="5qqGKGm4EaawnAH0J6xluc6AWdQBvLW3"
export UALA_STAGE_CLIENT_SECRET="cVp1iGEB-DE6KtL4Hi7tocdopP2pZxzaEVciACApWH92e8_Hloe8CD5ilM63NppG"
```

## 🔄 Flujo de Pago

### 1. Creación del Pedido

Cuando un cliente completa el formulario de checkout:

1. Se crea un `Pedido` en la base de datos con estado `pendiente`
2. Se crean los `ItemPedido` asociados
3. Se llama a la API de Ualá para crear una orden de pago
4. Se guarda el `uala_order_id` y `uala_checkout_url` en el pedido
5. El cliente es redirigido al checkout de Ualá

### 2. Procesamiento del Pago

El cliente completa el pago en el checkout de Ualá usando:
- Tarjeta de crédito
- Tarjeta de débito
- (Próximamente) Código QR

### 3. Webhook de Notificación

Ualá envía una notificación al webhook configurado (`/webhook/uala/`) cuando:
- El pago es aprobado
- El pago es rechazado
- La orden es cancelada

El webhook actualiza automáticamente el estado del pedido.

### 4. Verificación Manual

Si el webhook no se ejecuta, el estado se verifica automáticamente cuando el cliente visita la página de detalle del pedido.

## 📡 Endpoints

### Webhook de Ualá

**URL:** `/webhook/uala/`  
**Método:** POST  
**CSRF:** Deshabilitado (requerido por Ualá)

Este endpoint recibe notificaciones de Ualá sobre cambios en las órdenes.

### Detalle de Pedido

**URL:** `/pedido/<pedido_id>/`  
**Método:** GET

Muestra los detalles del pedido y verifica automáticamente el estado en Ualá si está pendiente.

## 🗄️ Modelo de Datos

### Campos Agregados al Modelo Pedido

- `uala_order_id`: ID de la orden en Ualá
- `uala_checkout_url`: URL para completar el pago
- `uala_status`: Estado del pago en Ualá
- `uala_payment_id`: ID del pago (cuando se completa)

### Estados del Pedido

- `pendiente`: Pedido creado, esperando pago
- `pagado`: Pago completado exitosamente
- `rechazado`: Pago rechazado o cancelado
- `completado`: Pedido completado (legacy)
- `cancelado`: Pedido cancelado (legacy)

## 🔧 Cliente Ualá

El módulo `tienda/uala_client.py` contiene la clase `UalaClient` que maneja:

- Autenticación con OAuth2 (client credentials)
- Creación de órdenes de pago
- Consulta del estado de órdenes
- Gestión automática de tokens (renovación cuando expiran)

## 🧪 Pruebas

### Entorno Stage

Por defecto, el sistema usa el entorno STAGE de Ualá. Puedes probar con tarjetas de prueba proporcionadas por Ualá.

### Configurar URL del Webhook

Para que los webhooks funcionen en desarrollo local, puedes usar herramientas como:
- [ngrok](https://ngrok.com/) para exponer tu servidor local
- [localtunnel](https://localtunnel.github.io/www/)

Ejemplo con ngrok:
```bash
ngrok http 8000
# Usar la URL proporcionada en SITE_URL
```

Luego actualiza `SITE_URL` en settings.py o como variable de entorno.

## 📚 Documentación de Ualá

- [Documentación API v2](https://developers.ualabis.com.ar/v2)
- [Autenticación](https://developers.ualabis.com.ar/v2#autenticaci%C3%B3n)
- [Crear Orden](https://developers.ualabis.com.ar/v2#post-crear-orden)
- [Webhooks](https://developers.ualabis.com.ar/v2#webhook-creaci%C3%B3n-de-orden)

## ⚠️ Notas Importantes

1. **Seguridad**: Nunca expongas las credenciales en el código. Usa variables de entorno en producción.

2. **Webhooks**: Asegúrate de que la URL del webhook sea accesible públicamente para que Ualá pueda enviar notificaciones.

3. **HTTPS**: En producción, siempre usa HTTPS para proteger las transacciones.

4. **Logs**: Revisa los logs del servidor para depurar problemas con la integración.

5. **Moneda**: Actualmente configurado para ARS (Pesos Argentinos). Si necesitas cambiar la moneda, edita `tienda/uala_client.py`.

## 🐛 Solución de Problemas

### Error al obtener token

- Verifica que las credenciales sean correctas
- Asegúrate de que la URL base sea correcta (stage vs prod)

### Webhook no se ejecuta

- Verifica que la URL sea accesible públicamente
- Revisa los logs del servidor
- Verifica que el endpoint no requiera autenticación

### Pedido no se actualiza

- El webhook puede no haberse ejecutado
- El estado se verifica automáticamente al visitar el detalle del pedido
- Puedes verificar manualmente desde el admin de Django

