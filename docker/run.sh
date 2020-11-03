#!/bin/sh

set -e

if [ ! -z "$RDS_HOSTNAME" ]; then
    echo "Amazon Relational Database detected: $RDS_HOSTNAME:$RDS_PORT"
    DB_ADDRESS="$RDS_HOSTNAME"
    DB_PORT="$RDS_PORT"
fi

echo "Waiting for database ..."
while ! pg_isready -h $DB_ADDRESS -p $DB_PORT 2>/dev/null; do
    sleep 1
done

echo "Making migrations ..."
ENV=production python2 manage.py makemigrations

echo "Migrating database ..."
ENV=production python2 manage.py migrate_schemas

echo "Compiling i18n messages ..."
ENV=production python2 manage.py compilemessages ||:

ENV=production  python2 manage.py runserver --help

export DJANGO_SETTINGS_MODULE=bluebottle.settings.local

echo "Starting debug server with live reload ..."
exec python2 manage.py runserver 0.0.0.0:8080

exit

exec \
    gunicorn bluebottle.settings.wsgi \
     --name=bluebottle \
     --user=$BLUEBOTTLE_USER --group=$BLUEBOTTLE_USER \
     --bind=0.0.0.0:8080 \
     --log-level=$LOG_LEVEL \
     --log-file=- \
     --worker-class=gevent
