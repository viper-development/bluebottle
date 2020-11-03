#!/bin/sh

set -e

echo "Starting debug server with live reload ..."
exec python2 manage.py runserver 0.0.0.0:8080
