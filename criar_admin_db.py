"""
Script para criar superusuário diretamente no banco de dados PostgreSQL do Render
Execute: python crear_admin_db.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juegos360.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

# URL do banco de dados do Render
DATABASE_URL = "postgresql://juegos_360:2uMOCJR984MmohsEIRKCwFvJN8dzfuw8@dpg-d5bho5ruibrs73cgcu00-a.virginia-postgres.render.com/juegos360"

# Configurar conexão direta
import dj_database_url
os.environ['DATABASE_URL'] = DATABASE_URL

# Credenciais do admin
USERNAME = 'admin'
EMAIL = 'admin@juegos360.com'
PASSWORD = 'admin123'

def criar_superusuario():
    """Cria superusuário diretamente no banco de dados"""
    try:
        # Verificar se o usuário já existe
        if User.objects.filter(username=USERNAME).exists():
            print(f"❌ O usuário '{USERNAME}' já existe!")
            print("Para alterar a senha, use o Django admin ou delete o usuário primeiro.")
            return False
        
        # Criar superusuário
        user = User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )
        
        print("✅ Superusuário criado com sucesso!")
        print(f"   Usuário: {USERNAME}")
        print(f"   Email: {EMAIL}")
        print(f"   Senha: {PASSWORD}")
        print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro acesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Conectando ao banco de dados do Render...")
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print("\nCriando superusuário...")
    criar_superusuario()

