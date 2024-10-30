from django.conf import settings

DEBUG = True
ALLOWED_HOSTS = ['*']

settings.INSTALLED_APPS += [
    'core',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simple_lms',
        'USER': 'simple_user',
        'PASSWORD': 'simple_password',
        'HOST': 'simple_db',
    }
}