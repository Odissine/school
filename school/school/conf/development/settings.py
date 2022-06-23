import os
import warnings
from django.utils.translation import ugettext_lazy as _
from os.path import dirname
from . import settings_private

warnings.simplefilter('error', DeprecationWarning)

BASE_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

SECRET_KEY = settings_private.SECRET_KEY

DEBUG = True
ALLOWED_HOSTS = ['192.168.1.145', 'localhost', '127.0.0.1', '192.168.1.118', 'endtg.pythonanywhere.com']

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_select2',
    'bootstrap5',
    'crispy_forms',
    'mathfilters',
    'crispy_bootstrap5',
    # Application Apps
    'account',
    'main',
    'games',
    'poll',
    'import_export',
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

ROOT_URLCONF = 'school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'school.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = settings_private.EMAIL_HOST
EMAIL_HOST_USER = settings_private.EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = settings_private.EMAIL_DEFAULT
EMAIL_HOST_PASSWORD = settings_private.EMAIL_HOST_PASSWORD
EMAIL_PORT = settings_private.EMAIL_PORT
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

API_GMASS = settings_private.API_GMASS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    #
    {
         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 3, }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = True
LOGIN_VIA_EMAIL_OR_USERNAME = False
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'account:login'
USE_REMEMBER_ME = True

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(CONTENT_DIR, 'static'),
)
STATIC_ROOT = os.path.join(CONTENT_DIR, 'assets')

MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')
MEDIA_URL = '/media/'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_CONNEXION = os.path.join(LOG_DIR, 'connexion.log')
open(LOG_CONNEXION, 'a').close()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'connexion_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOG_CONNEXION,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'accounts.views': {
            'level': 'INFO',
            'handlers': ['connexion_file'],
        },
    },
}

# GMAIL
config_mail = settings_private.CONFIG_MAIL
