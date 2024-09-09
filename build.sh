#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
