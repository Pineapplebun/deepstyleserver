FROM tensorflow/tensorflow:latest-gpu-py3

RUN mkdir /app
COPY requirements.txt /app/

COPY cuda/include/cudnn.h /usr/local/cuda/include
COPY cuda/lib64/libcudnn* /usr/local/cuda/lib64/
RUN chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
ENV CUDA_HOME=/usr/local/cuda

WORKDIR /app

RUN pip3 install -r requirements.txt

WORKDIR /app/neural-style

RUN apt-get update
RUN apt-get install -y wget
RUN wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
RUN apt-get install -y vim

EXPOSE 8000

WORKDIR /app

COPY dswebsite /app/dswebsite
COPY neural-style/ /app/neural-style
COPY start_app_wrapper.sh /app
COPY job_scheduler.py /app
COPY print_db.py /app
