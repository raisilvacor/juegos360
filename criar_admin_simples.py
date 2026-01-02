#!/usr/bin/env python
"""
Script simples para criar superusuário no Render
Execute no Shell do Render: python crear_admin_simples.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juegos360.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Credenciais
USERNAME = 'admin'
EMAIL = 'admin@juegos360.com'
PASSWORD = 'admin123'

try:
    # Verificar se existe
    if User.objects.filter(username=USERNAME).exists():
        print(f"⚠️  Usuário '{USERNAME}' já existe!")
        user = User.objects.get(username=USERNAME)
        # Atualizar senha
        user.set_password(PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"✅ Senha do usuário '{USERNAME}' foi atualizada!")
    else:
        # Criar novo
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"✅ Superusuário '{USERNAME}' criado com sucesso!")
    
    print(f"\n📋 Credenciais:")
    print(f"   Usuário: {USERNAME}")
    print(f"   Email: {EMAIL}")
    print(f"   Senha: {PASSWORD}")
    print(f"\n🌐 Acesse: https://juegos360.onrender.com/admin/")
    print(f"⚠️  IMPORTANTE: Altere a senha após o primeiro acesso!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()

