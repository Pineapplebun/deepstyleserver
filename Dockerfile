FROM tensorflow/tensorflow:latest-gpu-py3

COPY dswebsite /app/dswebsite
COPY neural-style/ /app/neural_style
COPY start_app_wrapper.sh /app
COPY job_scheduler.py /app
COPY requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80
