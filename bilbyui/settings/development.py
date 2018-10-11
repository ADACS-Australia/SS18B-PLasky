from .base import *

DEBUG = True

SITE_URL = 'http://127.0.0.1:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_FROM = 'ssaleheen@swin.edu.au'
EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bilby',
        'USER': 'root',
        'PASSWORD': 'your password',
    },
}

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['handlers'] = ['console', 'file']

try:
    from .local import *
except ImportError:
    pass
