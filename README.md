# Wagtail helpdesk

This repository holds the code for `wagtail-helpdesk`, a Wagtail app aimed at answering questions by experts. The original implementation was done for [Klimaathelpdesk](https://klimaathelpdesk.org), a website aimed at answering questions regarding climate change, global warming, and related.

[![License](https://img.shields.io/github/license/Klimaat-Helpdesk/wagtail-helpdesk)](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/wagtail-helpdesk.svg)](https://badge.fury.io/py/wagtail-helpdesk)
[![wagtail-helpdesk CI](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/actions/workflows/test.yml/badge.svg)](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/actions/workflows/test.yml)

## Links

- [Documentation](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/blob/main/README.md)
- [Questions, issues and bugs](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/issues)
- [Security](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/security)

## Supported versions

- Python 3.9, 3.10, 3.11
- Django 4.2 LTS
- Wagtail 5.2 LTS

## Installation

- Install the `wagtail-helpdesk` package:

  `$ pip install wagtail-helpdesk`

- Add the wagtail-helpdesk apps to your `INSTALLED_APPS` in your project's `settings.py`:
  ```python
    INSTALLED_APPS = [
        "wagtail_helpdesk",
        "wagtail_helpdesk.cms",
        "wagtail_helpdesk.core",
        "wagtail_helpdesk.experts",
        "wagtail_helpdesk.utils",
        "wagtail_helpdesk.volunteers",
        # Add all wagtail apps according to wagtail docs
        ...
        # Add wagtail routable page contrib module
        "wagtail.contrib.routable_page",
    ]
  ```

- Add the wagtail_helpdesk urls to your project's `urls.py`:
  ```python
  from wagtail_helpdesk.urls import urlpatterns as helpdesk_urlpatterns
  
  urlpatterns += [
      ...
      path("", include(wagtail_urls)),
      path("", include(helpdesk_urlpatterns)),
  ]
  ```


- Run Django migrations to create the database tables:

  `$ python manage.py migrate`
