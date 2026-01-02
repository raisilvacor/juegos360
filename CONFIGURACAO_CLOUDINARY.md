# Configuração do Cloudinary para Armazenamento de Imagens

## Por que Cloudinary?

O Render não mantém arquivos de mídia entre deploys ou durante hibernação. Para garantir que as imagens dos jogos sejam preservadas, usamos o Cloudinary, um serviço de armazenamento de mídia na nuvem.

## Como Configurar

### 1. Criar Conta no Cloudinary

1. Acesse https://cloudinary.com/
2. Crie uma conta gratuita (plano gratuito inclui 25GB de armazenamento)
3. Após criar a conta, você verá o Dashboard com suas credenciais

### 2. Obter Credenciais

No Dashboard do Cloudinary, você encontrará:
- **Cloud Name**: Nome da sua conta
- **API Key**: Chave de API
- **API Secret**: Segredo da API

### 3. Configurar no Render

No painel do Render, adicione estas variáveis de ambiente:

1. Vá em **Settings** → **Environment**
2. Adicione as seguintes variáveis:

```
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret
```

**IMPORTANTE**: Substitua os valores pelos seus dados reais do Cloudinary.

### 4. Banco de Dados PostgreSQL

O banco de dados já está configurado para usar PostgreSQL do Render. Certifique-se de que:

1. Um banco PostgreSQL foi criado no Render
2. A variável `DATABASE_URL` está configurada automaticamente pelo Render

## Benefícios

✅ **Imagens persistentes**: As imagens não serão perdidas durante deploys ou hibernação
✅ **Banco de dados persistente**: Todos os dados ficam no PostgreSQL do Render
✅ **Backup automático**: Cloudinary faz backup automático das imagens
✅ **CDN global**: Imagens são servidas rapidamente de qualquer lugar do mundo
✅ **Plano gratuito generoso**: 25GB de armazenamento gratuito

## Verificação

Após configurar, faça um deploy e teste:

1. Acesse o admin: `https://juegos360.onrender.com/admin/`
2. Crie ou edite um jogo
3. Faça upload de uma imagem
4. A imagem deve aparecer corretamente e ser armazenada no Cloudinary

## Notas

- Se as variáveis do Cloudinary não estiverem configuradas, o sistema usará armazenamento local (que será perdido em deploys)
- Para desenvolvimento local, você pode criar um arquivo `.env` com as credenciais do Cloudinary
- O plano gratuito do Cloudinary é suficiente para a maioria dos casos de uso

