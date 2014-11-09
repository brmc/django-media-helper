INSTALLED_APPS = [
    'media_helper',
]

SECRET_KEY = '1'

DEBUG = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = ('',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.db',
    }
}
