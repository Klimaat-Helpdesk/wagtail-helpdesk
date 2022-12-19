# Wagtail helpdesk

This repository holds the code for `wagtail-helpdesk`, a Wagtail app aimed at answering questions by experts. The original implementation was done for [Klimaathelpdesk](https://klimaathelpdesk.org), a website aimed at answering questions regarding climate change, global warming, and related.

[![License]![GitHub](https://img.shields.io/github/license/Klimaat-Helpdesk/wagtail-helpdesk)](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/wagtail-helpdesk.svg)](https://badge.fury.io/py/wagtail-helpdesk)
[![wagtail-helpdesk CI](https://github.com/fourdigits/wagtail-helpdesk/actions/workflows/test.yml/badge.svg)](https://github.com/fourdigits/wagtail-helpdesk/actions/workflows/test.yml)

## Links

- [Documentation](https://github.com/fourdigits/wagtail-helpdesk/blob/main/README.md)
- [Discussions](https://github.com/fourdigits/wagtail-helpdesk/discussions)
- [Security](https://github.com/fourdigits/wagtail-helpdesk/security)

## Supported versions

- Python 3.9, 3.10
- Django 3.2 LTS
- Wagtail 4.1 LTS

## Installation

- Add the wagtail-helpdesk apps to your `INSTALLED_APPS` in your project's `settings.py`:
  ```python
    INSTALLED_APPS = [
        "wagtail_helpdesk",
        "wagtail_helpdesk.cms",
        "wagtail_helpdesk.core",
        "wagtail_helpdesk.experts",
        "wagtail_helpdesk.utils",
        "wagtail_helpdesk.volunteers",
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
