"""
Django settings for CidProject project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from django.conf import global_settings

import os
import pymysql
from pathlib import Path
gettext = lambda s: s

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3(u(^9o#1x0a*w+r@2wf*84*dr*kect4iolwxxux$1uy))0n=y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ciddash.tlictprojects.com', 'cid.customs.gov.tl', '127.0.0.1', '10.8.0.21','localhost']


#Here the two lines I added
CSRF_TRUSTED_ORIGINS = ['https://ciddash.tlictprojects.com/']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    #'adminlte3',
     #'admin_two_factor.apps.TwoStepVerificationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cidApp',
    #'adminlte3',
    #'django_otp',
    #'django_otp.plugins.otp_static',
    #'django_otp.plugins.otp_totp',
    #'django_otp.plugins.otp_email',  # <- if you want email capability.
    #'two_factor',
   # 'two_factor.plugins.phonenumber',  # <- if you want phone number capability.
    #'two_factor.plugins.email',  # <- if you want email capability.
    #'two_factor.plugins.yubikey',  # <- for yubikey capability.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django_otp.middleware.OTPMiddleware',
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

pymysql.install_as_MySQLdb()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ciddash_new_db",
        "USER": "ict",
        "PASSWORD": "customs2024!",
        "HOST": "localhost",
        "PORT": "3306",
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
EXTRA_LANG_INFO = {
    'tl': {
        'bidi': True, # right-to-left
        'code': 'tl',
        'name': 'Tetum',
        'name_local': u'\u0626\u06C7\u064A\u063A\u06C7\u0631 \u062A\u0649\u0644\u0649', #unicode codepoints here
    },
}

# Add custom languages not provided by Django in this case TETUM has not yet included to django 
# so we have costumize to Tetum.
import django.conf.locale
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["tl"]


LANGUAGE_CODE = 'tl'

TIME_ZONE = 'UTC'

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
LANGUAGES_BIDI	=['he', 'ar', 'ar-dz', 'fa', 'ur']
print(
LOCALE_PATHS)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]


LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL ='/'

#LOGIN_URL = 'two_factor:login'

# this one is optional
#LOGIN_REDIRECT_URL = 'two_factor:profile'



#AUTH_USER_MODEL = 'cidApp.User' #updated
AUTHENTICATION_BACKENDS = ['cidApp.backends.EmailBackend'] #updated



EXTRA_LANG_INFO = {
    'tl': {
        'bidi': True, # right-to-left
        'code': 'tl',
        'name': 'Tetum',
        'name_local': u'\u0626\u06C7\u064A\u063A\u06C7\u0631 \u062A\u0649\u0644\u0649', #unicode codepoints here
    },
}

# Add custom languages not provided by Django
import django.conf.locale
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["tl"]


# Ensure the session engine is correct
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Session expires when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Session timeout (optional)
SESSION_COOKIE_AGE = 3600  # Session will expire in 1 hour (3600 seconds)