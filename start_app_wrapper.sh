#!/bin/sh
python3 /app/dswebsite/manage.py makemigrations
python3 /app/dswebsite/manage.py migrate
python3 /app/dswebsite/manage.py runserver &
python3 /app/job_scheduler.py 8 /app/dswebsite/db.sqlite3
wait
