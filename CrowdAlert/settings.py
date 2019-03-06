"""
Django settings for CrowdAlert project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
import dj_database_url
import pyrebase
import googlemaps
import firebase_admin

# Generate the Firebase Service Account Credential json file
with open('serviceAccountCredentials.json','w') as f:
    JSON_DATA = {}
    for key in os.environ.keys():
        if 'DJANGO_FIREBASE_' in key:
            JSON_DATA[key.strip('DJANGO_FIREBASE_')] = os.environ[key].replace("\\n",'\n')
    f.writelines(json.dumps(JSON_DATA))

CONFIG = {
    "apiKey": os.environ['REACT_APP_FIREBASE_API_KEY'],
    "authDomain": os.environ['REACT_APP_FIREBASE_AUTH_DOMAIN'],
    "databaseURL": os.environ['REACT_APP_FIREBASE_DATABASE_URL'],
    "storageBucket": os.environ['REACT_APP_FIREBASE_PROJECT_ID'] + ".appspot.com",
    "serviceAccount": "./serviceAccountCredentials.json"
}

cred = firebase_admin.credentials.Certificate(CONFIG["serviceAccount"])
FIREBASE_ADMIN = firebase_admin.initialize_app(cred)

# Instantiate a Firebase - Pyrebase object so that we can import later
FIREBASE = pyrebase.initialize_app(CONFIG)
GMAPS = googlemaps.Client(key=os.environ['REACT_APP_GOOGLE_MAPS_KEY'])


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z=(8l%o$v8-l-cx9kaah(+be@cwu0w5=pqnul24yf7w%svk87w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.events',
    'api.location',
    'api.images',
    'api.users',
    'api.comments',
    'corsheaders',
    'api.firebase_auth',
    'api.upvote',
    'api.spam',
    'api.notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
]

ROOT_URLCONF = 'CrowdAlert.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'build')
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

WSGI_APPLICATION = 'CrowdAlert.wsgi.application'

if os.environ.get("HEROKU", False):
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Collectstatic will copy js & css files
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'build/static'),
#   os.path.join(BASE_DIR, 'build/'),
]
# If we plan to use API wide authentication,
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'api.firebase_auth.authentication.TokenAuthentication', 
#     ),
# }
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Update database configuration with $DATABASE_URL.
DB_ENV = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(DB_ENV)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ORIGIN_WHITELIST = (    
    'crowdalert.herokuapp.com',
    'localhost:3000',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token',
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
