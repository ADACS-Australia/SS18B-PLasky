from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CONN_MAX_AGE = 900  # 15 minutes of persistent connection

EMAIL_FROM = ''
EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

STATIC_ROOT = os.path.join(BASE_DIR, '../static/')
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "../static/"),
    os.path.join(BASE_DIR, "../tupakweb/static/"),
    os.path.join(BASE_DIR, "../accounts/static/"),
]

ROOT_SUBDIRECTORY_PATH = 'projects/tupak/live/'
STATIC_URL = '/projects/tupak/live/static/'

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
