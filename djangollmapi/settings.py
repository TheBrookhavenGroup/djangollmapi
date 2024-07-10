import os
from os import environ as env
from pathlib import Path
import configparser
from tbgutils import dt as mc_dt
from django.core.management.utils import get_random_secret_key

config_file = os.path.join(os.getcwd(), 'djangollmapi', 'djangollmapi.config')
config_file = os.environ.get('DJANGO_LLM_API_CONFIG', config_file)

assert os.path.exists(config_file)
print(f"Config File: {config_file}")
config = configparser.ConfigParser(interpolation=None)
config.read(config_file)

ADMIN_URL = config['DJANGO']['ADMIN_URL']
DOMAIN = config['DJANGO']['DOMAIN']
PROJECT_NAME = config['DJANGO']['PROJECT_NAME']
SECRET_KEY = config['DJANGO']['SECRET_KEY']
ADMIN_URL = config['DJANGO']['ADMIN_URL']

POSTGRES_USER = config['POSTGRES']['USER']
POSTGRES_PASSWORD = config['POSTGRES']['PASS']
POSTGRES_DB = config['POSTGRES']['DB']

LLM_PACKAGE = config['LLM']['MODEL_PACKAGE']
LLM_MODELS = [config['LLM']['MODEL1'], config['LLM']['MODEL2']]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['DJANGO']['DEBUG'].lower() == 'true'

# Build paths inside the worth like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_VERSIONS = {}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', DOMAIN]

INSTALLED_APPS = [
    'users',
    'djangollmapi.apps.AdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'apis',
]

AUTH_USER_MODEL = 'users.Member'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangollmapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'djangollmapi/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['djangollmapi.templatetags.project_tags'],
        },
    },
]

WSGI_APPLICATION = 'djangollmapi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'HOST': '127.0.0.1',
        'PORT': 5432,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True
mc_dt.time_zone = TIME_ZONE

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'djangollmapi/static')
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# from kombu import Exchange, Queue
# CELERY_TASK_QUEUES = (
#     Queue('serial', Exchange('MarcExchange'), routing_key='MarcRoutingkey'),
# )

if env.get('EAGER_CELERY', False):
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    BROKER_BACKEND = 'memory'
