# Instruções para Deploy no Render

## Configuração no Render

### 1. Start Command
No campo **Start Command**, use:
```
gunicorn juegos360.wsgi:application
```

### 2. Build Command (opcional, mas recomendado)
No campo **Build Command**, use:
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### 3. Variáveis de Ambiente
Configure estas variáveis de ambiente no Render:

- `SECRET_KEY`: Gere uma chave secreta (pode usar: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `seu-app.onrender.com` (substitua pelo seu domínio do Render)
- `SITE_URL`: `https://seu-app.onrender.com` (URL completa do seu site no Render)
- `MERCADOPAGO_ACCESS_TOKEN`: Seu token do Mercado Pago
- `MERCADOPAGO_PUBLIC_KEY`: Sua chave pública do Mercado Pago
- `MERCADOPAGO_CLIENT_ID`: Seu Client ID do Mercado Pago
- `MERCADOPAGO_CLIENT_SECRET`: Seu Client Secret do Mercado Pago

### 4. Banco de Dados
- O Render pode criar um PostgreSQL automaticamente
- Ou você pode usar SQLite (não recomendado para produção)
- Se usar PostgreSQL, adicione `psycopg2-binary` ao `requirements.txt`

### 5. Arquivos Estáticos
- Os arquivos estáticos serão servidos pelo WhiteNoise (já configurado)
- O `collectstatic` será executado no Build Command

### 6. Arquivos de Mídia
- Para uploads de imagens, considere usar um serviço como AWS S3 ou Cloudinary
- Ou configure o Render para servir arquivos de mídia

## Notas Importantes

1. **SITE_URL**: Configure com a URL completa do seu site no Render (ex: `https://juegos360.onrender.com`)
2. **Webhooks do Mercado Pago**: Configure a URL do webhook como `https://seu-app.onrender.com/webhook/mercadopago/`
3. **HTTPS**: O Render fornece HTTPS automaticamente, necessário para o Mercado Pago funcionar corretamente

