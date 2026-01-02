"""
WSGI config for juegos360 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juegos360.settings')

# Tentar executar migrações automaticamente na inicialização (apenas se necessário)
try:
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    # Verificar se as tabelas existem
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables or len(tables) < 5:  # Se não houver tabelas suficientes
            logger.info("Executando migrações automaticamente...")
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
except Exception as e:
    logger.warning(f"Erro ao executar migrações automaticamente: {e}")

application = get_wsgi_application()
