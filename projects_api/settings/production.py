import json

from .base import *
from .base import env

# GENERAL
# --------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['api.simonmartineau.dev', ]

# STORAGE
# --------------------------------------------------------------------------------
INSTALLED_APPS += ['storages']
AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}

AWS_LOCATION = 'drs'

# STATIC
# ---------------------------
STATICFILES_STORAGE = 'apps.core.utils.storages.StaticRootS3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/static/'

# MEDIA
# ---------------------------
DEFAULT_FILE_STORAGE = "portfolio_api.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/media/'

# MIDDLEWARE
# --------------------------------------------------------------------------------
MIDDLEWARE.insert(1, 'apps.core.middleware.HideAdminMiddleware')  # Insert after security middleware
# Hide admin page for certain ips

# HIDE ADMIN
# --------------------------------------------------------------------------------
HIDE_ADMIN_ALLOWED_IPS = env('DJANGO_ADMIN_WHITELIST_IPS').split(",")

# REST FRAMEWORK
# --------------------------------------------------------------------------------
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer', ]

# SECURITY
# --------------------------------------------------------------------------------
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header
# This tells django that requests with this header are secure (https is handled by the proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS
# --------------------------------------------------------------------------------
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
INSTALLED_APPS += ['corsheaders']

CORS_ALLOWED_ORIGINS = [
    'https://simonmartineau.dev'
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^(https?://(?:.+\.)?localhost(?::\d{1,5})?)$"
]

# DATABASE
# --------------------------------------------------------------------------------
# parse the database url
DATABASES = {
    'default': env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# LOGGING
# --------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
