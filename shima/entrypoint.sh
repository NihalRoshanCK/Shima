#!/bin/sh

echo 'Waiting for postgres...'
echo 'Running migrations...'
python manage.py migrate

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo "migration and staticfile configured successfully."

exec "$@"