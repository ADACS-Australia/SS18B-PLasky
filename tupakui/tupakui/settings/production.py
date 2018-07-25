from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CONN_MAX_AGE = 900  # 15 minutes of persistent connection

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
