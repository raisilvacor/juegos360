"""
Django settings for juegos360 project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - incluir domínio do Render por padrão
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
else:
    # Por padrão, permitir todos os domínios do Render e localhost
    ALLOWED_HOSTS = ['juegos360.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Para armazenar mídia no Cloudinary
    'cloudinary',  # SDK do Cloudinary
    'tienda',  # Nuestra app de la tienda
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir arquivos estáticos no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'juegos360.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tienda.context_processors.carrito',  # Context processor para el carrito
            ],
        },
    },
]

WSGI_APPLICATION = 'juegos360.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Database
# Usar PostgreSQL se DATABASE_URL estiver definido (Render), senão SQLite
try:
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=600)
    if db_from_env:
        DATABASES = {
            'default': db_from_env
        }
    else:
        # Fallback para SQLite se DATABASE_URL não estiver definido
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
except ImportError:
    # Se dj_database_url não estiver instalado, usar SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
except Exception as e:
    # Em caso de erro, usar SQLite como fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para collectstatic no Render

# Configuração do WhiteNoise para servir arquivos estáticos
# WhiteNoise já está configurado no MIDDLEWARE
# Configurar WhiteNoise para servir arquivos de media também (se não usar Cloudinary)
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Media files (uploads) - Usar Cloudinary para armazenamento persistente
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuração do Cloudinary (usar variáveis de ambiente)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

# Se Cloudinary estiver configurado, usar para armazenamento
if CLOUDINARY_STORAGE.get('CLOUD_NAME'):
    try:
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    except:
        # Se cloudinary_storage não estiver disponível, continuar com local
        pass

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.environ.get('MERCADOPAGO_ACCESS_TOKEN', 'APP_USR-6061576205385432-010119-e1efc6c461af6484480958359679c579-1770535202')
MERCADOPAGO_PUBLIC_KEY = os.environ.get('MERCADOPAGO_PUBLIC_KEY', 'APP_USR-62c633e1-7ce5-432c-a46a-96723200b844')
MERCADOPAGO_CLIENT_ID = os.environ.get('MERCADOPAGO_CLIENT_ID', '6061576205385432')
MERCADOPAGO_CLIENT_SECRET = os.environ.get('MERCADOPAGO_CLIENT_SECRET', 'npiLIARVUC97jYGAJ6iaZKvvpppOuKns')

# Activar/desactivar Mercado Pago
MERCADOPAGO_ENABLED = True  # Cambiar a False para desactivar temporalmente

# URL base del sitio (para webhooks)
SITE_URL = os.environ.get('SITE_URL', 'http://127.0.0.1:8000')
