import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fz*b)@9p-evq92vf$b%@y)e6o28(muir0$je@m)o%+-l$a&(v_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG', True))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

RABBITMQ_HOST='rabbitmq'
BOOK_RABBITMQ_QUEUE = 'book_creation_que'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    "rest_framework_simplejwt",
    # 'celery',

    "drf_yasg",

    "Book",
    "User"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookworm.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'bookworm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

MONGO_DB_NAME = os.environ.get('MONGO_DB', 'bookworm')
MONGO_DB_USERNAME = os.environ.get('MONGO_USERNAME', 'admin')
MONGO_DB_PASSWORD = os.environ.get('MONGO_PASSWORD', 'password')
MONGO_DB_HOST = os.environ.get('MONGO_HOST', '127.0.0.1')
MONGO_DB_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DB_URI = os.environ.get('MONGO_URI',"")


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'CLIENT': {
            'host': MONGO_DB_URI,
            'username': MONGO_DB_USERNAME,
            'password': MONGO_DB_PASSWORD,
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}
AUTH_USER_MODEL = 'User.User'


# Celery Configuration
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://admin:password@rabbitmq:5672/')
# CELERY_RESULT_BACKEND = 'rpc://'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
REFRESH_TOKEN_LIFETIME = timedelta(minutes=60)


