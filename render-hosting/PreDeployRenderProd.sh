#!/usr/bin/env bash
# Exit on error
set -o errexit
python manage.py collectstatic --no-input --settings=settings.render-prod
# Apply any outstanding database migrations
python manage.py makemigrations --settings=settings.render-prod
python manage.py migrate --settings=settings.render-prod