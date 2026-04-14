from .base import *  # NOQA

INSTALLED_APPS += [
    # "debug_toolbar",
]

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

BASE_URL = WAGTAILADMIN_BASE_URL = "http://localhost:8000"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}

DEBUG = True

# Django should serve static, frontend service (npm run start) will auto rebuild
STORAGES = {
    "default": {"BACKEND": "apps.core.storages.MediaS3Storage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
}
# Project has no docker-compose, use filesystem for media
#STORAGES["default"] = {
#    "BACKEND": "django.core.files.storage.FileSystemStorage"
#}
STATIC_URL = "/static/"
STATIC_ROOT = "/static/"

# Project has no docker-compose, use filesystem for media
#STORAGES["default"] = {  # noqa: F405
#    "BACKEND": "django.core.files.storage.FileSystemStorage"
#}
MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / "media")
MEDIA_URL = "/media/"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

