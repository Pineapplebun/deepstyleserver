#!/bin/sh

# Install Docker CE and replace ec2-user
# The first argument of this script is the ec2-user
sudo apt-get update
sudo apt-get install -y docker-ce
sudo usermod -a -G docker $1

# Install Nvidia Drivers
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt-get update
sudo apt-get install -y nvidia-375 nvidia-settings nvidia-modprobe

# Install Nvidia Docker
sudo apt-get update
sudo apt-get install \ apt-transport-https \ ca-certificates \ curl \ software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \ “deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable”


# Setup Nvidia Docker
# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb
# Test if docker is using nvidia GPUs
nvidia-docker run — rm nvidia/cuda nvidia-smi

# Install NVIDIA-DOCKER-COMPOSE
sudo pip install nvidia-docker-compose


# Build Docker Container and run it
# -p is port, -d is detach, -it is interactive terminal
# CPU and web server: docker run -p 80:80 -v /..folder../src/:/var/www/html

nvidia-docker-compose build
nvidia-docker-compose up -d
