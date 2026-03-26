#!/usr/bin/env bash
# Exit on error
set -o errexit
#npm run --quiet build 
python manage.py collectstatic --no-input --settings=settings.render-test
# Apply any outstanding database migrations
python manage.py makemigrations --settings=settings.render-test
python manage.py migrate --settings=settings.render-test