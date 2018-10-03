from .development import *

DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.sqlite3',
    },
}

TEST_OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'test_output')

LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['loggers']['bilbyweb']['handlers'] = ['file']
