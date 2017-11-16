#!/bin/sh
sleep 10 &&
python /app/dswebsite/manage.py makemigrations &&
python /app/dswebsite/manage.py migrate &&
python /app/dswebsite/manage.py collectstatic --no-input &&
cd dswebsite &&
gunicorn dswebsite.wsgi -b 0.0.0.0:8000 &
sleep 30 &&
python /app/job_scheduler.py 8 &
wait
