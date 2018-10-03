from .base import *

DEBUG = True

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
    LOGGING['loggers'][logger]['handlers'] = ['console']

try:
    from .local import *
except ImportError:
    pass
