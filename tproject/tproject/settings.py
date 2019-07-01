"""
Django settings for tproject project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import requests
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '28=yz63c!&j%zmk#h!e$@-co#byb$7g#3_x6$fuh80-rb-ip=h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'qrcode',
    'imagekit',
    'taxiapp',
    'location_field.apps.DefaultConfig',
    'bootstrap3',
    'mod_wsgi.server',
    'storages',
    'rest_framework',
    'rest_framework_swagger',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

)

ROOT_URLCONF = 'tproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


#WSGI_APPLICATION = 'tproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
    'default': {
       # Server Configuration
       #  'ENGINE': 'django.db.backends.postgresql_psycopg2',
       #  'NAME': 'taxidb',
       #  'HOST': 'taxiapp-2.cdbkqvigkoct.ap-south-1.rds.amazonaws.com',
       #  'PORT': 5432,
       #  'USER': 'valv_admin',
       #  'PASSWORD': 'Bharath360',
	# End of Server Configuration
    # Local Configuration
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'postgres',
        'PORT': 5432,
    # End of Local Configuration
    # Docker Configuration
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
    #     'USER': os.environ.get('POSTGRES_USER', 'postgres'),
    #     'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    #     'HOST': os.environ.get('POSTGRES_HOST', 'host.docker.internal'),
    #     'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        #     # End of Docker Configuration
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'taxiapp.MyUser'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'taxiapp/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'taxiapp/media')
GOOGLE_URL_SHORTENER_KEY = "AIzaSyDNWWg5dCIxZYiO8uo6wkPEdDUb2NwdFs4"

LOCATION_FIELD_PATH = STATIC_URL + 'location_field'

LOCATION_FIELD = {
    'map.provider': 'google',
    'map.zoom': 14,

    'search.provider': 'google',
    'search.suffix': '',

    # Google
    'provider.google.api': '//maps.google.com/maps/api/js',
    'provider.google.api_key': 'AIzaSyBX_xC2Jeti6f0v83GVrnzX0mvfDyZE9yc',
    'provider.google.map_type': 'ROADMAP',

    # Mapbox
#    'provider.mapbox.access_token': '',
#    'provider.mapbox.max_zoom': 18,
#    'provider.mapbox.id': 'mapbox.streets',

    # OpenStreetMap
    'provider.openstreetmap.max_zoom': 18,

    # misc
    'resources.root_path': LOCATION_FIELD_PATH,
    'resources.media': {
        'js': [
            LOCATION_FIELD_PATH + '/js/jquery.livequery.js',
            LOCATION_FIELD_PATH + '/js/form.js',
        ],
    },
}


# S3 settings

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'taxipublic'
AWS_ACCESS_KEY_ID = 'AKIAJXIBCZNZCKK4S6JQ'
AWS_SECRET_ACCESS_KEY = 'GOTf2y7ThWOcUt4FRb8XmmJDjt6lM9Y1ZQoNH8QB'
AWS_DEFAULT_ACL = "public-read" # to make sure all your files gives read only access to the files

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_HOST = 's3.ap-south-1.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = 's3.ap-south-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
AWS_QUERYSTRING_AUTH = False
S3DIRECT_REGION = 'ap-south-1'
# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
S3_URL = "https://%s" % AWS_S3_CUSTOM_DOMAIN
# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATIC_DIRECTORY = '/static/'
MEDIA_DIRECTORY = '/media/'

'https://taxipublic.s3.ap-south-1.amazonaws.com/media/drivers/DSCN2533.JPG'
AWS_S3_MEDIA_DOMAIN = 'https://%s.s3.ap-south-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = AWS_S3_MEDIA_DOMAIN + MEDIA_DIRECTORY
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

TEMPLATE_DEBUG = DEBUG

try:
    EC2_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
    ALLOWED_HOSTS.append(EC2_IP)
except requests.exceptions.RequestException:
    pass
