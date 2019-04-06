#!/usr/bin/env bash
./make_requirements.sh
./node_modules/.bin/gulp build
./.venv/bin/python manage.py collectstatic --noinput
