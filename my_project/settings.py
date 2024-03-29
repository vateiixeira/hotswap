import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x4&en%b6kbe4+z&y+7&0iqtf9gx%g8tt)c@gh&vhc+$5-c6wq0'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

from decouple import config, Csv

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'my_project.core',
    'my_project.estoque',
    'my_project.chamado',
    'my_project.envios',
    'my_project.transf',
    'my_project.frentecaixa',
    'my_project.atendimento',
    'my_project.msg',
    'my_project.compras',
    'my_project.base',
    'my_project.api',
    'my_project.helpdesk',
    'my_project.ws',

    'django_select2',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'solo',
    'channels'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_project.urls'

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'my_project.wsgi.application'
ASGI_APPLICATION = 'my_project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'teste',
#         'USER': 'root',
#         'PASSWORD': '1',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME', default='hotswap'),
        'USER': config('DB_USER'),
        'PASSWORD':  config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# REDIRECIONA APOS FEITO LOGIN
LOGIN_URL = 'core:login'
#LOGIN_REDIRECT_URL = 'core:homepage'
# REDIRECIONA APOS LOGOUT
LOGOUT_REDIRECT_URL = 'core:logout'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-mail.outlook.com'
#EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = config('EMAIL_USER')
FROM_EMAIL = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')


# celery
BROKER_URL = config('BROKER_URL')
# CELERY REDIS
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_SEND_EVENTS=True
CELERY_TIMEZONE = TIME_ZONE


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
   "http://localhost:8080",
   "https://192.168.1.222",
   "http://192.168.1.222",
]

import datetime 
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=18),
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
}