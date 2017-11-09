#!/bin/bash

# starting gunicorn
echo Starting gunicorn
exec gunicorn dswebsite.wsgi:application \
				--bind 0.0.0.0:8000 \
				--workers 3
