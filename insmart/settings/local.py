from insmart.settings.base import *

DEBUG = True
INSTALLED_APPS += (
    'debug_toolbar', # and other apps for local development
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)