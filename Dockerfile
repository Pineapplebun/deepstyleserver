FROM tensorflow/tensorflow:latest-gpu-py3

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

WORKDIR /app/neural-style

RUN apt-get update
RUN apt-get install -y wget
RUN wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat

EXPOSE 8000

WORKDIR /app

COPY dswebsite /app/dswebsite
COPY neural-style/ /app/neural-style
COPY start_app_wrapper.sh /app
COPY job_scheduler.py /app
