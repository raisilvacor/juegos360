# Instruções para Acessar o Admin

## Problema
Não consegue acessar o admin porque não há superusuário criado no banco de dados.

## Solução 1: Usar o Comando Automático (Recomendado)

O sistema agora cria automaticamente um superusuário durante o build com estas credenciais padrão:

- **Usuário**: `admin`
- **Email**: `admin@juegos360.com`
- **Senha**: `admin123`

**IMPORTANTE**: Altere a senha após o primeiro acesso!

## Solução 2: Criar Manualmente via Shell do Render

1. No painel do Render, vá em **Shell** (ou use o terminal)
2. Execute:
   ```bash
   python manage.py crear_superusuario --username admin --email admin@juegos360.com --password admin123
   ```

## Solução 3: Usar Variáveis de Ambiente (Mais Seguro)

No painel do Render, configure estas variáveis de ambiente:

```
ADMIN_USERNAME=seu-usuario
ADMIN_EMAIL=seu-email@exemplo.com
ADMIN_PASSWORD=sua-senha-segura
```

Depois, execute no shell:
```bash
python manage.py crear_superusuario
```

O comando usará automaticamente as variáveis de ambiente.

## Solução 4: Criar via Django Shell

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

## Após Criar o Superusuário

1. Acesse: `https://juegos360.onrender.com/admin/`
2. Faça login com as credenciais criadas
3. **IMPORTANTE**: Altere a senha imediatamente após o primeiro acesso!

## Segurança

⚠️ **NUNCA** deixe a senha padrão em produção!

Após criar o superusuário, altere a senha:
1. Faça login no admin
2. Vá em **Usuários** → Selecione seu usuário
3. Altere a senha para algo seguro

