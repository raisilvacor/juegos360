# Solución para Error 403 - Ualá Bis

## Problema

Error `403 Forbidden` con mensaje "Missing Authentication Token" al intentar obtener el token de autenticación de Ualá Bis.

## Posibles Causas

1. **Credenciales incorrectas o expiradas**: Las credenciales de Stage o Producción pueden haber expirado o ser incorrectas.
2. **Endpoint incorrecto**: El endpoint de autenticación puede haber cambiado.
3. **Formato de petición incorrecto**: La API puede requerir un formato específico.

## Soluciones

### 1. Verificar Credenciales

Las credenciales están en `juegos360/settings.py`. Verifica que sean correctas:

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

### 2. Probar con Comando de Diagnóstico

Ejecuta el comando de prueba:

```bash
python manage.py test_uala
```

Para probar con credenciales de producción:

```bash
python manage.py test_uala --production
```

### 3. Contactar con Soporte de Ualá

Si las credenciales no funcionan:

1. **Email de soporte técnico**: developers.ualabis@uala.com.ar
2. **Documentación**: https://developers.ualabis.com.ar/v2
3. Solicita:
   - Verificación de credenciales
   - Nuevas credenciales si han expirado
   - Confirmación del endpoint correcto de autenticación

### 4. Verificar Documentación Actualizada

La documentación oficial está en: https://developers.ualabis.com.ar/v2

Revisa la sección de "Autenticación" para confirmar:
- El endpoint correcto
- El formato de la petición
- Los parámetros requeridos

### 5. Alternativa Temporal

Mientras se resuelve el problema con Ualá, puedes:

1. **Desactivar temporalmente la integración**: Comentar el código que crea la orden en Ualá
2. **Usar modo simulación**: Permitir crear pedidos sin pago real
3. **Contactar con Ualá**: Para obtener credenciales válidas o verificar el problema

## Código Actualizado

El código ya está actualizado para:
- Intentar primero con `application/x-www-form-urlencoded` (formato OAuth2 estándar)
- Si falla, intentar con `application/json`
- Mostrar mensajes de error más descriptivos

## Próximos Pasos

1. Verifica las credenciales con el equipo de Ualá
2. Prueba con nuevas credenciales si las actuales han expirado
3. Revisa la documentación actualizada de Ualá Bis API v2
4. Contacta con soporte técnico si el problema persiste

## Nota Importante

Las credenciales de Stage pueden tener una validez limitada. Si estás usando credenciales de prueba, es posible que necesites solicitar nuevas credenciales a Ualá.

