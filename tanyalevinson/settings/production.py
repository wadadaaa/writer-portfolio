from .base import *

DEBUG = False
print("Production")
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False

project = 'tanyalevinson'

DEFAULT_FILE_STORAGE = 'tanyalevinson.s3.Media'
STATICFILES_STORAGE = 'tanyalevinson.s3.CachedS3BotoStorage'
MEDIA = 'media'
MEDIA_ROOT = MEDIA

STATIC = 'static'
STATIC_ROOT = STATIC

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = 'tanyalevinson.s3.Static'
COMPRESS_OFFLINE = False