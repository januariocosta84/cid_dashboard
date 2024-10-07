
from django.conf import global_settings
import os
import pymysql
from pathlib import Path
gettext = lambda s: s
import environ
import django.conf.locale
pymysql.install_as_MySQLdb()

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

SRF_TRUSTED_ORIGINS = [env('CSRF_TRUSTED_ORIGINS')]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cidApp',
     'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CidProject.urls'
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

WSGI_APPLICATION = 'CidProject.wsgi.application'
DATABASES = {
    "default": {
        "ENGINE": env('DATABASE_ENGINE'),
        "NAME": env('DATABASE_NAME'),
        "USER": env('DATABASE_USER'),
        "PASSWORD": env('DATABASE_PASSWORD'),
        "HOST": env('DATABASE_HOST'),
        "PORT": env('DATABASE_PORT'),
    }
}

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

STATIC_URL = env('STATIC_URL')
MEDIA_URL = env('MEDIA_URL')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_ROOT = env('MEDIA_ROOT')
STATICFILES_DIRS = [env('STATICFILES_DIRS')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = env('LOGIN_URL')
LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL')

# Custom Authentication Backend
AUTHENTICATION_BACKENDS = [env('AUTHENTICATION_BACKENDS')]

# Session Settings
SESSION_ENGINE = env('SESSION_ENGINE')
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool('SESSION_EXPIRE_AT_BROWSER_CLOSE')
SESSION_COOKIE_AGE = env.int('SESSION_COOKIE_AGE')


# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


# Add custom languages not provided by Django in this case TETUM has not yet included to django 
# so we have costumize to Tetum.
EXTRA_LANG_INFO = {
    'tl': {
        'bidi': True, # right-to-left
        'code': 'tl',
        'name': 'Tetum',
        'name_local': u'\u0626\u06C7\u064A\u063A\u06C7\u0631 \u062A\u0649\u0644\u0649', #unicode codepoints here
    },
}
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["tl"]
LANGUAGE_CODE = 'tl'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = False
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGES =[
        ('en', 'English'),
        ('id', 'Indonesia'),
        ('tl', 'Tetum'),
        ('pt', 'Portugues'),
        ('tl', gettext('Tetum'))
]