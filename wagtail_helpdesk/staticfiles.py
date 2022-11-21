"""
This file is heavily based on Wagtail's staticfiles loader:
https://github.com/wagtail/wagtail/blob/main/wagtail/admin/staticfiles.py
"""

import hashlib

from django.conf import settings
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.core.files.storage import get_storage_class
from django.templatetags.static import static

from wagtail_helpdesk import __version__


def get_version_hash(version_string):
    if settings.DEBUG:
        # Hashed filenames are disabled in debug mode, so keep the querystring
        use_version_strings = True
    else:
        # see if we're using a storage backend using hashed filenames
        storage = get_storage_class(settings.STATICFILES_STORAGE)
        use_version_strings = not issubclass(storage, HashedFilesMixin)

    if use_version_strings:
        return hashlib.sha1((version_string + settings.SECRET_KEY).encode("utf-8")).hexdigest()[:8]


def versioned_static(path):
    """
    Wrapper for Django's static file finder to append a cache-busting query parameter
    that updates on each Wagtail version
    """
    # An absolute path is returned unchanged (either a full URL, or processed already)
    if path.startswith(("http://", "https://", "/")):
        return path

    base_url = static(path)

    version_hash = get_version_hash(__version__)
    # if URL already contains a querystring, don't add our own, to avoid interfering
    # with existing mechanisms
    if version_hash is None or "?" in base_url:
        return base_url
    else:
        return base_url + "?v=" + version_hash
