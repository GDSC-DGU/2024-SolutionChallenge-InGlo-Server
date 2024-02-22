#!/bin/sh

python3 manage.py collectstatic --noinput

# cron 서비스 시작
cron

# Django 서버 시작
python3 manage.py runserver 0.0.0.0:8000