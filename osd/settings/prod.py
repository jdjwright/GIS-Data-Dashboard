from .base import *
from .secret import *

DEBUG = True

ALLOWED_HOSTS = ['www.greenpen.net',
]

SECURE_SSL_REDIRECT = True


STATIC_URL = '/static/'
STATIC_ROOT = '/home/greenpen/OSD/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = '/home/greenpen/OSD/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')