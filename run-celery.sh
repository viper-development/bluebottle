#!/bin/sh

celery worker -A bluebottle.celery --loglevel=INFO
