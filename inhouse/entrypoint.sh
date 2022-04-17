#!/bin/sh


echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done
echo "PostgreSQL started"

# It's okay to run the following two, flush and migrate commands on development mode(when debug mode is on) but not recommended
# for production:

# python manage.py flush --no-input
# python manage.py migrate

exec "$@"