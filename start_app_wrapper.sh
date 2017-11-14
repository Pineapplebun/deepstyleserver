#!/bin/sh
python /app/dswebsite/manage.py makemigrations &&
python /app/dswebsite/manage.py migrate &&
cd dswebsite &&
gunicorn dswebsite.wsgi -b 0.0.0.0:8000 &
sleep 20 &&
python3 /app/job_scheduler.py 1 &
wait
