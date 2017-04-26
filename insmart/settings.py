"""
Django settings for insmart project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '21(3m0lphxuf=r@onw4#$-6kvf)z(8ylrk4i5yy(5uv7r%#x$g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'secure-atoll-90896.herokuapp.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'vendors',
    'product',
    'axes',
    'user_management',
    'inventory',
    'alert',
    'insmart_core',
    'pagination_bootstrap'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'insmart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'insmart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'insmart',
        'USER': 'insmart',
        'PASSWORD': 'insmart',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '../static/'),
)

LOGIN_REDIRECT_URL = 'home'


# for password reset emails
# https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'box797.bluehost.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'insmart@jameswarlick.com'
EMAIL_HOST_PASSWORD = 'zNDJBuCFSyb;4zz'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'insmart@jameswarlick.com'


# for Django Axes (session lockout stuff)
# See https://django-axes.readthedocs.io/en/latest/configuration.html#customizing-axes for more.
AXES_LOCKOUT_URL = 'lockout'                # Where to send a locked out IP address
AXES_COOLOFF_TIME = 1                       # Number of hours until the lockout is "forgotten"
AXES_LOGIN_FAILURE_LIMIT = 5                # How many is too many?
AXES_LOCK_OUT_AT_FAILURE = True             # Toggle switch for the whole plugin.


# Session Expiration Settings
# See https://docs.djangoproject.com/en/dev/topics/http/sessions/#session-save-every-request
SESSION_SAVE_EVERY_REQUEST = True           # Unoptimized method of keeping the session alive.
SESSION_COOKIE_AGE = 155 * 60               # Expire the session after 15 minutes of inactivity