import os
from datetime import timedelta

from pets_search_service.settings.env_reader import env


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG')

SERVER_HOST = env.str('SERVER_HOST')

ALLOWED_HOSTS = [
    SERVER_HOST,
]

INSTALLED_APPS = [
    # Extensions
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'rest_framework.authtoken',
    # Project applications
    'apps.users.apps.UsersConfig',
    'apps.pet_adoption_notices.apps.PetAdoptionNoticesConfig',
    'apps.pet_missing_notices.apps.PetMissingNoticesConfig',
    'apps.pet_found_notices.apps.PetFoundNoticesConfig',
    'apps.pet_notice_matches.apps.PetNoticeMatchesConfig',
    'apps.complaints.apps.ComplaintsConfig',
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

ROOT_URLCONF = 'pets_search_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pets_search_service.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
    },
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('ACCESS_TOKEN_LIFETIME_MINUTES', 60)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'UPDATE_LAST_LOGIN': True,
}

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'bucket_name': env.str('MINIO_BUCKET_NAME'),
            'endpoint_url': env.str('MINIO_ENDPOINT'),
            'custom_domain': env.str('MINIO_EXTERNAL_URL'),
            'access_key': env.str('MINIO_ROOT_USER'),
            'secret_key': env.str('MINIO_ROOT_PASSWORD'),
            'querystring_auth': False,
            'file_overwrite': False,
        },
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

AUTH_USER_MODEL = 'users.User'

TIME_ZONE = 'Asia/Yekaterinburg'
USE_TZ = True

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'ru'
LANGUAGES = (('ru', 'Русский'),)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/ev_api/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
