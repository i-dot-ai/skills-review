#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate --noinput
python manage.py initialise_taxonomy
watchmedo auto-restart --directory=./  --pattern=""*.py"" --recursive -- python manage.py runserver 0.0.0.0:8008 --noreload
