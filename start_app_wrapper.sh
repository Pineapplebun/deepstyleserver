#!/bin/sh
<<<<<<< HEAD
python3 /app/dswebsite/manage.py makemigrations
python3 /app/dswebsite/manage.py migrate
python3 /app/dswebsite/manage.py runserver &
python3 /app/job_scheduler.py 8 /app/dswebsite/db.sqlite3
=======
python /app/dswebsite/manage.py makemigrations &&
python /app/dswebsite/manage.py migrate &&
cd dswebsite &&
gunicorn dswebsite.wsgi -b 0.0.0.0:8000 &&
python3 /app/job_scheduler.py 1 /app/dswebsite/db.sqlite3
>>>>>>> 6c491b8ee7456fe155a25bd1c3f40c7d59e41a46
wait
