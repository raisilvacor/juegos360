# Instrucciones para Resolver Error 403 con Ualá

## Problema Actual

Estás recibiendo el error:
```
Error 403 al obtener token: Missing Authentication Token
```

Esto significa que las credenciales de Ualá no son válidas o han expirado.

## Solución Inmediata: Desactivar Ualá Temporalmente

Mientras resuelves el problema con las credenciales, puedes desactivar temporalmente la integración con Ualá:

1. Abre el archivo `juegos360/settings.py`
2. Busca la línea:
   ```python
   UALA_ENABLED = True
   ```
3. Cámbiala a:
   ```python
   UALA_ENABLED = False
   ```

Con esto, los pedidos se crearán normalmente pero sin integración de pago. Los clientes podrán ver sus pedidos pero no podrán pagar hasta que actives Ualá nuevamente.

## Solución Permanente: Obtener Credenciales Válidas

### Paso 1: Contactar con Soporte de Ualá

**Email de soporte técnico**: developers.ualabis@uala.com.ar

**Información a solicitar:**
- Verificación de credenciales actuales
- Nuevas credenciales de Stage (si las actuales expiraron)
- Confirmación del endpoint correcto de autenticación
- Documentación actualizada de la API v2

### Paso 2: Verificar Credenciales

Las credenciales están en `juegos360/settings.py`:

**Para STAGE (pruebas):**
```python
UALA_STAGE_USERNAME = 'new_user_1631906477'
UALA_STAGE_CLIENT_ID = '5qqGKGm4EaawnAH0J6xluc6AWdQBvLW3'
UALA_STAGE_CLIENT_SECRET = 'cVp1iGEB-DE6KtL4Hi7tocdopP2pZxzaEVciACApWH92e8_Hloe8CD5ilM63NppG'
```

**Para PRODUCCIÓN:**
```python
UALA_USERNAME = 'raisilva.smt'
UALA_CLIENT_ID = 'eqbz8x1nFczDlKA6bVjRM86gy0BMUvrw'
UALA_CLIENT_SECRET = 'Sowk0d0fzHe1F-LmuOxj6RBSDk6y7zrdHxBq74sg_knMqCNLplMDxgECf1Ieq_sX'
```

### Paso 3: Actualizar Credenciales

Cuando recibas las nuevas credenciales:

1. Actualiza los valores en `juegos360/settings.py`
2. O usa variables de entorno:
   ```bash
   export UALA_STAGE_USERNAME="nuevo_username"
   export UALA_STAGE_CLIENT_ID="nuevo_client_id"
   export UALA_STAGE_CLIENT_SECRET="nuevo_secret"
   ```

### Paso 4: Probar la Conexión

Ejecuta el comando de prueba:

```bash
python manage.py test_uala
```

Si funciona, verás:
```
✓ Token obtenido exitosamente!
```

### Paso 5: Reactivar Ualá

Una vez que las credenciales funcionen:

1. Abre `juegos360/settings.py`
2. Cambia:
   ```python
   UALA_ENABLED = True
   ```
3. Reinicia el servidor Django

## Documentación de Ualá

- **Documentación oficial**: https://developers.ualabis.com.ar/v2
- **Email de soporte**: developers.ualabis@uala.com.ar

## Notas Importantes

1. **Credenciales de Stage**: Pueden tener una validez limitada. Si expiran, necesitarás solicitar nuevas.

2. **Credenciales de Producción**: Son permanentes pero más sensibles. No las compartas públicamente.

3. **Modo sin Ualá**: Cuando `UALA_ENABLED = False`, los pedidos se crean normalmente pero sin procesamiento de pago. Esto es útil para desarrollo o cuando hay problemas con la API.

4. **Logs**: Revisa los logs del servidor Django para ver detalles de los errores.

## Estado Actual

- ✅ Código de integración listo
- ✅ Manejo de errores implementado
- ❌ Credenciales necesitan ser validadas/actualizadas
- ⚠️ Ualá puede ser desactivado temporalmente

