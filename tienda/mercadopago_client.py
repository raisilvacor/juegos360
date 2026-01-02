"""
Cliente para integración con Mercado Pago
Documentación: https://www.mercadopago.com.ar/developers/es/docs
"""
import requests
import json
from django.conf import settings
from django.utils import timezone


class MercadoPagoClient:
    """Cliente para interactuar con la API de Mercado Pago"""
    
    def __init__(self):
        self.access_token = getattr(settings, 'MERCADOPAGO_ACCESS_TOKEN', '')
        self.public_key = getattr(settings, 'MERCADOPAGO_PUBLIC_KEY', '')
        self.client_id = getattr(settings, 'MERCADOPAGO_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'MERCADOPAGO_CLIENT_SECRET', '')
        
        if not self.access_token:
            raise Exception("MERCADOPAGO_ACCESS_TOKEN no configurado en settings.py")
    
    def _get_headers(self):
        """Obtiene los headers con el token de autenticación"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def crear_preferencia(self, pedido, items, back_urls=None):
        """
        Crea una preferencia de pago en Mercado Pago
        
        Args:
            pedido: Instancia del modelo Pedido
            items: Lista de items del pedido
            back_urls: Dict con success, failure, pending (opcional)
        
        Returns:
            dict con la respuesta de la API (init_point, preference_id, etc.)
        """
        url = "https://api.mercadopago.com/checkout/preferences"
        
        # Construir items para Mercado Pago
        mp_items = []
        for item in items:
            mp_items.append({
                "title": item.juego.titulo[:127],  # Limitar longitud
                "quantity": int(item.cantidad),
                "unit_price": float(item.precio),  # Precio en ARS
                "currency_id": "ARS"  # Pesos argentinos
            })
        
        # Construir URLs - SOLO usar URLs válidas y públicas
        site_url = getattr(settings, 'SITE_URL', '').strip()
        
        # Si es localhost o 127.0.0.1, NO incluir notification_url (no es válido para Mercado Pago)
        # notification_url es OPCIONAL - solo necesario para webhooks en producción
        is_local = not site_url or '127.0.0.1' in site_url or 'localhost' in site_url
        
        # Para back_urls, usar el site_url o un placeholder válido
        # En desarrollo local, las back_urls pueden ser locales (el usuario volverá manualmente)
        if not site_url:
            site_url = 'http://127.0.0.1:8000'  # Para back_urls en desarrollo
        
        # Si no se pasaron back_urls, construir los default
        if not back_urls or not isinstance(back_urls, dict):
            back_urls = {}
        
        # Construir back_urls - FORMATO EXACTO requerido por Mercado Pago
        back_urls_final = {
            "success": back_urls.get("success", f"{site_url}/pedido/{pedido.id}/?status=approved"),
            "failure": back_urls.get("failure", f"{site_url}/pedido/{pedido.id}/?status=rejected"),
            "pending": back_urls.get("pending", f"{site_url}/pedido/{pedido.id}/?status=pending")
        }
        
        # Construir el payload - FORMATO EXACTO según documentación de Mercado Pago
        payload = {
            "items": mp_items,
            "payer": {
                "name": pedido.nombre_cliente.split()[0] if pedido.nombre_cliente.split() else pedido.nombre_cliente,
                "surname": " ".join(pedido.nombre_cliente.split()[1:]) if len(pedido.nombre_cliente.split()) > 1 else "",
                "email": pedido.email
            },
            "back_urls": back_urls_final,
            "external_reference": str(pedido.id)
        }
        
        # SOLO agregar notification_url si NO es localhost (debe ser URL pública HTTPS)
        # notification_url es OPCIONAL - el checkout funciona sin él
        if not is_local and site_url.startswith('https://'):
            payload["notification_url"] = f"{site_url}/webhook/mercadopago/"
        
        try:
            headers = self._get_headers()
            
            # Debug: verificar payload antes de enviar
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"[MP] Creando preferencia para pedido {pedido.id}")
            logger.info(f"[MP] back_urls.success: {back_urls_final.get('success')}")
            logger.info(f"[MP] Payload keys: {list(payload.keys())}")
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            logger.info(f"[MP] Status code: {response.status_code}")
            
            if response.status_code not in [200, 201]:
                error_detail = f"Status {response.status_code}"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict):
                        # Mercado Pago devuelve errores en formato específico
                        if 'message' in error_data:
                            error_detail = error_data['message']
                        elif 'error' in error_data:
                            error_detail = error_data['error']
                        elif 'cause' in error_data:
                            causes = error_data.get('cause', [])
                            if causes:
                                error_messages = []
                                for cause in causes:
                                    if isinstance(cause, dict):
                                        error_messages.append(cause.get('description', str(cause)))
                                    else:
                                        error_messages.append(str(cause))
                                error_detail = f"{error_data.get('message', '')} - {'; '.join(error_messages)}"
                            else:
                                error_detail = error_data.get('message', str(error_data))
                        else:
                            error_detail = str(error_data)
                    else:
                        error_detail = str(error_data)
                except:
                    error_detail = response.text[:500] or error_detail
                
                raise Exception(f"Error al crear preferencia en Mercado Pago: {error_detail}")
            
            return response.json()
            
        except Exception as e:
            # Si es nuestra excepción, re-lanzarla
            if "Error al crear preferencia" in str(e) or "back_urls.success" in str(e):
                raise
            # Si es otra excepción, convertirla
            raise Exception(f"Error al crear preferencia en Mercado Pago: {str(e)}")
    
    def obtener_pago(self, payment_id):
        """
        Obtiene el estado de un pago
        
        Args:
            payment_id: ID del pago en Mercado Pago
        
        Returns:
            dict con la información del pago
        """
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
        
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener pago de Mercado Pago: {str(e)}")
    
    def obtener_preferencia(self, preference_id):
        """
        Obtiene el estado de una preferencia
        
        Args:
            preference_id: ID de la preferencia en Mercado Pago
        
        Returns:
            dict con la información de la preferencia
        """
        url = f"https://api.mercadopago.com/checkout/preferences/{preference_id}"
        
        try:
            headers = self._get_headers()
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener preferencia de Mercado Pago: {str(e)}")
