"""
Script alternativo: Cria superusuário usando SQL direto no PostgreSQL
Útil quando o Django não consegue se conectar
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import hashlib
import secrets
import string

# Configurações do banco de dados
DB_HOST = "dpg-d5bho5ruibrs73cgcu00-a.virginia-postgres.render.com"
DB_NAME = "juegos360"
DB_USER = "juegos_360"
DB_PASSWORD = "2uMOCJR984MmohsEIRKCwFvJN8dzfuw8"

# Credenciais do admin
USERNAME = 'admin'
EMAIL = 'admin@juegos360.com'
PASSWORD = 'admin123'

def criar_superusuario_sql():
    """Cria superusuário usando SQL direto"""
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar se o usuário já existe
        cursor.execute("SELECT id FROM auth_user WHERE username = %s", (USERNAME,))
        if cursor.fetchone():
            print(f"❌ O usuário '{USERNAME}' já existe!")
            cursor.close()
            conn.close()
            return False
        
        # Gerar hash da senha (Django usa PBKDF2)
        from django.contrib.auth.hashers import make_password
        import os
        import sys
        import django
        
        # Configurar Django para usar a função de hash
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juegos360.settings')
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        django.setup()
        
        password_hash = make_password(PASSWORD)
        
        # Inserir usuário
        cursor.execute("""
            INSERT INTO auth_user (username, email, password, is_superuser, is_staff, is_active, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (USERNAME, EMAIL, password_hash, True, True, True))
        
        print("✅ Superusuário criado com sucesso!")
        print(f"   Usuário: {USERNAME}")
        print(f"   Email: {EMAIL}")
        print(f"   Senha: {PASSWORD}")
        print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro acesso!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Conectando ao PostgreSQL do Render...")
    print(f"Host: {DB_HOST}")
    print(f"Database: {DB_NAME}")
    print("\nCriando superusuário...")
    criar_superusuario_sql()

