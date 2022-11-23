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
    description="This repository holds the code for https://www.klimaathelpdesk.org, a website aimed at answering questions regarding climate change, global warming, and related.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Four Digits",
    author_email="info@fourdigits.nl",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
        "Framework :: Wagtail :: 4.1",
    ],
    install_requires=[
        "Django>=3.1,<4.0",
        "Wagtail>=2.0,<4.2",
        "django-allauth==0.44.0",
        "django-crispy-forms==1.11.0",
        "python-gitlab==2.5.0",
    ],
    extras_require={
        "testing": [
            "dj-database-url<1",  # 1.0.0 requires django 3.2
            "freezegun>=0.3.15,<2",
            "pytest<8",
            "factory-boy<3",  # 3.0 requires refactoring of factories
            "pytest-django<5",
            "pytest-cov<5",
        ],
    },
    zip_safe=False,
)
