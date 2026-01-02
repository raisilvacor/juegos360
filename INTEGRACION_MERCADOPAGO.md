# Integración con Mercado Pago - Juegos360

Esta documentación explica cómo funciona la integración con Mercado Pago para procesar pagos en la tienda de juegos Xbox 360.

## 📋 Configuración

### Credenciales

Las credenciales están configuradas en `juegos360/settings.py`:

```python
MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-6061576205385432-010119-e1efc6c461af6484480958359679c579-1770535202'
MERCADOPAGO_PUBLIC_KEY = 'APP_USR-62c633e1-7ce5-432c-a46a-96723200b844'
MERCADOPAGO_CLIENT_ID = '6061576205385432'
MERCADOPAGO_CLIENT_SECRET = 'npiLIARVUC97jYGAJ6iaZKvvpppOuKns'
```

### Variables de Entorno (Opcional)

También puedes configurar las credenciales usando variables de entorno:

```bash
export MERCADOPAGO_ACCESS_TOKEN="tu_access_token"
export MERCADOPAGO_PUBLIC_KEY="tu_public_key"
export MERCADOPAGO_CLIENT_ID="tu_client_id"
export MERCADOPAGO_CLIENT_SECRET="tu_client_secret"
```

## 🔄 Flujo de Pago

### 1. Creación del Pedido

Cuando un cliente completa el formulario de checkout:

1. Se crea un `Pedido` en la base de datos con estado `pendiente`
2. Se crean los `ItemPedido` asociados
3. Se llama a la API de Mercado Pago para crear una preferencia de pago
4. Se guarda el `mp_preference_id` y `mp_checkout_url` (init_point)` en el pedido
5. El cliente es redirigido al checkout de Mercado Pago

### 2. Procesamiento del Pago

El cliente completa el pago en el checkout de Mercado Pago usando:
- Tarjeta de crédito
- Tarjeta de débito
- Dinero en cuenta de Mercado Pago
- Otros métodos disponibles en Argentina

### 3. Retorno del Cliente

Después del pago, Mercado Pago redirige al cliente a:
- `success`: Si el pago fue aprobado
- `failure`: Si el pago fue rechazado
- `pending`: Si el pago está pendiente

### 4. Webhook de Notificación

Mercado Pago envía una notificación al webhook configurado (`/webhook/mercadopago/`) cuando:
- El pago es aprobado
- El pago es rechazado
- El estado del pago cambia

El webhook actualiza automáticamente el estado del pedido.

## 📡 Endpoints

### Webhook de Mercado Pago

**URL:** `/webhook/mercadopago/`  
**Método:** POST, GET  
**CSRF:** Deshabilitado (requerido por Mercado Pago)

Este endpoint recibe notificaciones de Mercado Pago sobre cambios en los pagos.

### Detalle de Pedido

**URL:** `/pedido/<pedido_id>/`  
**Método:** GET

Muestra los detalles del pedido y verifica automáticamente el estado si hay parámetros en la URL.

## 🗄️ Modelo de Datos

### Campos Agregados al Modelo Pedido

- `mp_preference_id`: ID de la preferencia en Mercado Pago
- `mp_checkout_url`: URL para completar el pago (init_point)
- `mp_status`: Estado del pago en Mercado Pago
- `mp_payment_id`: ID del pago (cuando se completa)

### Estados del Pedido

- `pendiente`: Pedido creado, esperando pago
- `pagado`: Pago completado exitosamente
- `rechazado`: Pago rechazado o cancelado
- `completado`: Pedido completado (legacy)
- `cancelado`: Pedido cancelado (legacy)

## 💰 Moneda

**Todos los precios están en Pesos Argentinos (ARS)**

- Los precios se muestran con el símbolo "$" y "ARS"
- Mercado Pago procesa los pagos en ARS
- Los items se envían a Mercado Pago con `currency_id: "ARS"`

## 🔧 Cliente Mercado Pago

El módulo `tienda/mercadopago_client.py` contiene la clase `MercadoPagoClient` que maneja:

- Creación de preferencias de pago
- Consulta del estado de pagos
- Consulta del estado de preferencias
- Autenticación con Access Token

## 🧪 Pruebas

### Modo Sandbox

Para pruebas, puedes usar las credenciales de sandbox de Mercado Pago. Las credenciales actuales son de producción.

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

## 📚 Documentación de Mercado Pago

- [Documentación API](https://www.mercadopago.com.ar/developers/es/docs)
- [Checkout Pro](https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/landing)
- [Webhooks](https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/webhooks)

## ⚠️ Notas Importantes

1. **Seguridad**: Nunca expongas las credenciales en el código. Usa variables de entorno en producción.

2. **Webhooks**: Asegúrate de que la URL del webhook sea accesible públicamente para que Mercado Pago pueda enviar notificaciones.

3. **HTTPS**: En producción, siempre usa HTTPS para proteger las transacciones.

4. **Logs**: Revisa los logs del servidor para depurar problemas con la integración.

5. **Moneda**: Todos los precios deben estar en ARS (Pesos Argentinos).

## 🐛 Solución de Problemas

### Error al crear preferencia

- Verifica que el Access Token sea correcto
- Asegúrate de que los precios sean números válidos
- Verifica que la URL del webhook sea accesible

### Webhook no se ejecuta

- Verifica que la URL sea accesible públicamente
- Revisa los logs del servidor
- Verifica que el endpoint no requiera autenticación

### Pedido no se actualiza

- El webhook puede no haberse ejecutado
- El estado se verifica automáticamente al retornar del checkout
- Puedes verificar manualmente desde el admin de Django

