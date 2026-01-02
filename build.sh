#!/usr/bin/env bash
set -o errexit

echo "=== Instalando dependências ==="
pip install -r requirements.txt

echo "=== Executando migrações ==="
python manage.py migrate --noinput

echo "=== Coletando arquivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Build concluído! ==="

