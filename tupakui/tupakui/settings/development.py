from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tupak',
        'USER': 'root',
        'PASSWORD': 'your password',
    },
}

try:
    from .local import *
except ImportError:
    pass
