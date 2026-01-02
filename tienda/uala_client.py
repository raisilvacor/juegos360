"""
Cliente para integración con Ualá Bis API v2
Documentación: https://developers.ualabis.com.ar/v2
"""
import requests
import json
from django.conf import settings
from django.utils import timezone


class UalaClient:
    """Cliente para interactuar con la API de Ualá Bis"""
    
    def __init__(self):
        # Determinar si estamos en producción o stage
        # Según documentación: https://developers.ualabis.com.ar/v2/orders/create
        self.is_production = getattr(settings, 'UALA_PRODUCTION', False)
        
        if self.is_production:
            # Producción: https://checkout.developers.ar.ua.la/v2/api
            self.base_url = "https://checkout.developers.ar.ua.la/v2/api"
            self.client_id = getattr(settings, 'UALA_CLIENT_ID', '')
            self.client_secret = getattr(settings, 'UALA_CLIENT_SECRET', '')
            self.username = getattr(settings, 'UALA_USERNAME', '')
        else:
            # Stage: https://checkout.stage.developers.ar.ua.la/v2/api
            self.base_url = "https://checkout.stage.developers.ar.ua.la/v2/api"
            self.client_id = getattr(settings, 'UALA_STAGE_CLIENT_ID', '')
            self.client_secret = getattr(settings, 'UALA_STAGE_CLIENT_SECRET', '')
            self.username = getattr(settings, 'UALA_STAGE_USERNAME', '')
        
        self.token = None
        self.token_expires_at = None
    
    def _get_token(self):
        """
        Obtiene un token de acceso usando client credentials
        """
        # Si tenemos un token válido, lo reutilizamos
        if self.token and self.token_expires_at:
            if timezone.now() < self.token_expires_at:
                return self.token
        
        # Verificar que tenemos las credenciales necesarias
        if not self.username or not self.client_id or not self.client_secret:
            env = "producción" if self.is_production else "stage"
            raise Exception(f"Credenciales de Ualá ({env}) no configuradas correctamente. Verifica settings.py")
        
        # Solicitar nuevo token
        # Según la documentación oficial: https://developers.ualabis.com.ar/v2/authentication/create
        # El endpoint de autenticación es: https://auth.developers.ar.ua.la/v2/api/auth/token
        # Para stage: https://auth.stage.developers.ar.ua.la/v2/api/auth/token (probablemente)
        if self.is_production:
            url = "https://auth.developers.ar.ua.la/v2/api/auth/token"
        else:
            # Para stage, probar diferentes variantes
            url = "https://auth.stage.developers.ar.ua.la/v2/api/auth/token"
        
        # Formato según documentación oficial de Ualá Bis
        # Verificar el formato exacto requerido por la API
        # El error 400 indica que el payload tiene campos incorrectos
        # Formato según documentación oficial: el campo es "username" (SIN guión bajo)
        payload = {
            "username": self.username,  # "username" según documentación oficial
            "client_id": self.client_id,
            "client_secret_id": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        # Debug: mostrar qué estamos enviando (sin el secret)
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Intentando autenticar con user_name: {self.username}, client_id: {self.client_id[:10]}...")
        
        try:
            # El error 415 indica que necesitamos form-urlencoded, NO JSON
            # Usar data=payload para enviar como form-urlencoded
            # Remover Content-Type explícito - dejar que requests lo maneje automáticamente
            response = requests.post(
                url,
                data=payload,  # requests automáticamente usa form-urlencoded
                headers={
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            # Si falla con 415, probar con JSON
            if response.status_code == 415:
                response = requests.post(
                    url,
                    json=payload,
                    headers={
                        'Accept': 'application/json'
                    },
                    timeout=10
                )
            
            # Si hay error, obtener más detalles
            if response.status_code != 200:
                error_detail = f"Status {response.status_code}"
                try:
                    error_data = response.json()
                    # El error 400 puede tener más detalles en 'errors' o 'message'
                    if 'errors' in error_data:
                        errors_list = error_data.get('errors', [])
                        error_detail = f"{error_data.get('message', '')} - Errores: {', '.join(str(e) for e in errors_list)}"
                    else:
                        error_detail = error_data.get('message') or error_data.get('error') or str(error_data)
                except:
                    error_detail = response.text[:500] or error_detail
                
                # Mensaje más descriptivo para error 400
                if response.status_code == 400:
                    raise Exception(
                        f"Error 400 - Payload inválido: {error_detail}. "
                        f"Verifica que los campos username, client_id y client_secret_id sean correctos. "
                        f"Endpoint: {url}"
                    )
                else:
                    raise Exception(f"Error {response.status_code} al obtener token: {error_detail}. Endpoint: {url}")
            
            response.raise_for_status()
            
            token_data = response.json()
            self.token = token_data.get('access_token')
            
            if not self.token:
                raise Exception("No se recibió access_token en la respuesta de Ualá")
            
            # Calcular expiración (normalmente 3600 segundos)
            expires_in = token_data.get('expires_in', 3600)
            from datetime import timedelta
            self.token_expires_at = timezone.now() + timedelta(seconds=expires_in - 60)  # 1 minuto de margen
            
            return self.token
            
        except requests.exceptions.HTTPError as e:
            error_detail = f"HTTP {response.status_code}"
            try:
                error_data = response.json()
                error_detail = error_data.get('message') or error_data.get('error') or str(error_data)
            except:
                error_detail = response.text if hasattr(response, 'text') else str(e)
            
            env = "producción" if self.is_production else "stage"
            raise Exception(f"Error al obtener token de Ualá ({env}): {error_detail}. Verifica las credenciales.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión con Ualá: {str(e)}")
    
    def _get_headers(self):
        """Obtiene los headers con el token de autenticación"""
        token = self._get_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def crear_orden(self, pedido, items, webhook_url=None):
        """
        Crea una orden de pago en Ualá
        Según documentación: https://developers.ualabis.com.ar/v2/orders/create
        
        Args:
            pedido: Instancia del modelo Pedido
            items: Lista de items del pedido
            webhook_url: URL para recibir notificaciones (opcional)
        
        Returns:
            dict con la respuesta de la API (checkout_link, uuid, etc.)
        """
        # Endpoint según documentación: POST /checkout
        url = f"{self.base_url}/checkout"
        
        # Construir descripción de los items
        descripcion_items = []
        for item in items:
            descripcion_items.append(f"{item.cantidad}x {item.juego.titulo}")
        
        descripcion = " | ".join(descripcion_items)
        if len(descripcion) > 200:
            descripcion = descripcion[:197] + "..."
        
        # Construir URLs de callback
        site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        callback_success = f"{site_url}/pedido/{pedido.id}/?status=success"
        callback_fail = f"{site_url}/pedido/{pedido.id}/?status=failed"
        
        # Construir el payload según la documentación oficial de Ualá
        # amount debe ser string, no número
        # Formato: https://developers.ualabis.com.ar/v2/orders/create
        payload = {
            "amount": str(pedido.total),  # String según documentación
            "description": descripcion,
            "callback_fail": callback_fail,
            "callback_success": callback_success,
            "external_reference": str(pedido.id)  # ID del pedido como referencia externa
        }
        
        # Agregar notification_url si está configurado (opcional)
        if webhook_url:
            payload["notification_url"] = webhook_url
        
        try:
            headers = self._get_headers()
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Error desconocido"
            try:
                error_data = response.json()
                error_detail = error_data.get('message', str(e))
            except:
                error_detail = str(e)
            
            raise Exception(f"Error al crear orden en Ualá: {error_detail}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión con Ualá: {str(e)}")
    
    def obtener_orden(self, order_id):
        """
        Obtiene el estado de una orden
        
        Args:
            order_id: ID de la orden en Ualá
        
        Returns:
            dict con la información de la orden
        """
        url = f"{self.base_url}/api/v2/orders/{order_id}"
        
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener orden de Ualá: {str(e)}")

