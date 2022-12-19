#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from wagtail_helpdesk import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail-helpdesk",
    version=__version__,
    description="A Wagtail app aimed at answering questions by experts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Four Digits",
    author_email="info@fourdigits.nl",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 4.1",
    ],
    install_requires=[
        "Django>=3.2,<4.0",
        "Wagtail>=3.0,<4.2",
        "django-allauth>=0.44,<1.0",
        "django-crispy-forms>=1.0,<2.0",
        "argon2-cffi>=21.0,<22.0",
    ],
    extras_require={
        "testing": [
            "dj-database-url>=1,<2",
            "pytest>=7,<8",
            "factory-boy>=3,<4",
            "pytest-django>=4,<5",
            "pytest-cov>=4,<5",
            "wagtail-factories>=3,<4",
            "django-webtest>=1,<2",
        ],
    },
    zip_safe=False,
)
