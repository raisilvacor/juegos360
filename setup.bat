@echo off
echo ====================================
echo   Juegos360 - Setup Inicial
echo ====================================
echo.

echo [1/5] Instalando dependencias...
pip install -r requirements.txt
echo.

echo [2/5] Aplicando migraciones...
python manage.py migrate
echo.

echo [3/5] Creando superusuario (opcional)...
echo Presiona Enter para omitir o ingresa los datos del superusuario
python manage.py createsuperuser
echo.

echo [4/5] Poblando base de datos con juegos de ejemplo...
python manage.py poblar_juegos
echo.

echo [5/5] Creando directorios necesarios...
if not exist "media\juegos" mkdir media\juegos
echo.

echo ====================================
echo   Setup completado!
echo ====================================
echo.
echo Para iniciar el servidor, ejecuta:
echo   python manage.py runserver
echo.
echo Luego abre en tu navegador:
echo   http://127.0.0.1:8000/
echo.
pause

