from .base import *  # noqa: F403



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


#del(STORAGES)

ALLOWED_HOSTS = []
DEBUG = False
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS.append("www.klimaathelpdesk.org")
ALLOWED_HOSTS.append("www2.klimaathelpdesk.org")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

MEDIA_ROOT = "/media"
MEDIA_URL = "/media/"

# store static files in deployment, not in Minio
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "formatters": {
        "default": {
            "verbose": "[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s"
        }
    },
    "loggers": {
        "klimaat-helpdesk": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "verbose",
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "formatter": "verbose",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
            "formatter": "verbose",
        },
        "django.security": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
            "formatter": "verbose",
        },
    },
}

# Render: schrijf static naar deze map (bestaat in runtime)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Render: override ALLEEN staticfiles storage (laat default media S3 met rust)
STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
}
# mandatory for Whitenoise to work
WHITENOISE_USE_FINDERS = True
WHITENOISE_ROOT = os.path.join(BASE_DIR, "staticfiles")
# # This production code might break development mode, so we check whether we're in DEBUG mode
# if not DEBUG:
#     # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#     # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
#     # and renames the files with unique names for each version to support long-term caching
#     STORAGES["staticfiles"] = {  # noqa: F405
#     "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
# }

GITLAB_PERSONAL_TOKEN= get_secret(
    os.getenv("GITLAB_PERSONAL_TOKEN_FILE", "/run/secrets/gitlab_personal_token"), ""
)
GITLAB_PROJECT_ID=14981988


