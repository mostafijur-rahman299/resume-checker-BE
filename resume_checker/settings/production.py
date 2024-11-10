
# Production settings

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['resumechecker-be.mostafijur.xyz', '103.191.50.57']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

