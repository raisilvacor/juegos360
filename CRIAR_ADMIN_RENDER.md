# Como Criar Superusuário no Render

## Opção 1: Usar o Script Python (Recomendado)

1. No painel do Render, vá em **Shell** (ou use SSH)
2. Execute:
   ```bash
   python crear_admin_db.py
   ```

## Opção 2: Usar Django Shell

1. No Render, vá em **Shell**
2. Execute:
   ```bash
   python manage.py shell
   ```
3. No shell Python, execute:
   ```python
   from django.contrib.auth import get_user_model
   User = get_user_model()
   User.objects.create_superuser('admin', 'admin@juegos360.com', 'admin123')
   ```

## Opção 3: Usar o Comando de Gerenciamento

1. No Render, vá em **Shell**
2. Execute:
   ```bash
   python manage.py crear_superusuario --username admin --email admin@juegos360.com --password admin123
   ```

## Opção 4: SQL Direto (Se nada funcionar)

1. Conecte-se ao PostgreSQL do Render usando um cliente (pgAdmin, DBeaver, etc)
2. Execute este SQL:

```sql
-- Primeiro, gere o hash da senha usando Django
-- Ou use este hash pré-gerado para senha 'admin123':
-- (Execute no Django shell: from django.contrib.auth.hashers import make_password; print(make_password('admin123')))

-- Depois insira o usuário:
INSERT INTO auth_user (username, email, password, is_superuser, is_staff, is_active, date_joined)
VALUES (
    'admin',
    'admin@juegos360.com',
    'pbkdf2_sha256$600000$...',  -- Substitua pelo hash gerado
    true,
    true,
    true,
    NOW()
);
```

## Credenciais Padrão

- **Usuário**: `admin`
- **Email**: `admin@juegos360.com`
- **Senha**: `admin123`

⚠️ **IMPORTANTE**: Altere a senha após o primeiro acesso!

## Verificar se Funcionou

1. Acesse: `https://juegos360.onrender.com/admin/`
2. Faça login com as credenciais acima
3. Se funcionar, altere a senha imediatamente!

