#!/bin/sh
python3 /app/dswebsite/manage.py runserver &
python3 /app/job_scheduler.py 8 /app/django_folder/db/db_filename
wait

# use CMD ["sh", "/app/start_app_wrapper.sh"] in Dockerfile
