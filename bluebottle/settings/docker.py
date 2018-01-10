# flake8: noqa
from os import environ as env, path
from bluebottle.settings.base import *

SECRET_KEY = env.get('SECRET_KEY', 'create a long random string here')
DEBUG = env.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = env.get('ALLOWED_HOSTS', '*').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'HOST': env.get('DB_HOST', 'localhost'),
        'PORT': env.get('DB_PORT', '5432'),
        'NAME': env.get('DB_NAME', 'bluebottle'),
        'USER': env.get('DB_USER', 'bluebottle'),
        'PASSWORD': env.get('DB_PASSWORD', 'bluebottle')
    }
}

CREATE_DB_EXTENSIONS = True

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

EMAIL_BACKEND = "bluebottle.utils.email_backend.DKIMBackend"
EMAIL_HOST = env.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = env.get('EMAIL_PORT', '1025')
EMAIL_USE_TLS = env.get('EMAIL_USE_TLS', 'False').lower() == 'true'

SEND_MAIL = env.get('SEND_MAIL', 'True').lower() == 'true'
SEND_WELCOME_MAIL = env.get('SEND_WELCOME_MAIL', 'True').lower() == 'true'

MEDIA_ROOT = env.get('MEDIA_ROOT', path.join(PROJECT_ROOT, 'static', 'media'))

TENANT_BASE = env.get('TENANT_BASE', path.join(PROJECT_ROOT, 'static', 'media'))

PRIVATE_MEDIA_ROOT = env.get('PRIVATE_MEDIA_ROOT', path.join(PROJECT_ROOT, 'private', 'media'))

MULTI_TENANT_DIR = env.get('MULTI_TENANT_DIR', path.join(PROJECT_ROOT, 'tenants'))
