from traveler.settings.base import *
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# CUSTOM
DATABASE_URL = os.environ.get("DATABASE_URL")

db_from_env = dj_database_url.config(default=DATABASE_URL)

DATABASES = {
    'default': db_from_env
}

#
# # AWS - Credentials
#
# AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
#
# # AWS - Media
#
# DEFAULT_FILE_STORAGE = 'traveler.settings.storage_backends.MediaStorage'  # <-- here is where we reference it
