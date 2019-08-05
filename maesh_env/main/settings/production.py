from ._base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['payments.maesh.io']

SITE = 'http://payments.maesh.io:8000/'

# To only have cookies to be sent over https
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'payments',
        'USER': 'maesh',
        'PASSWORD': 'z6E*A$R#09suwTjlM!DN',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#BACKUP FOR DATABASE?