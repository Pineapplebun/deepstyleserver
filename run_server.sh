## THIS IS A CHECKLIST OF THINGS TO INSTALL ON EC2
## DO NOT RUN THIS AS A SCRIPT! THERE MAY ALSO BE ARGUMENTS TO REPLACE
## FOLLOW THIS TUTORIAL: https://github.com/NVIDIA/nvidia-docker/wiki/Deploy-on-Amazon-EC2
## AFTER INSTALLING DOCKER CE AND DOCKER COMPOSE

# Install Docker CE and replace ec2-user
# The first argument of this script is the ec2-user
sudo yum update
sudo yum install -y docker-ce
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker COMPOSE
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Install Docker Machine
curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

# PROVISION AN EC2-GPU INSTANCE
docker-machine create --driver amazonec2 \
                      --amazonec2-region us-west-2 \
                      --amazonec2-zone b \
                      --amazonec2-ami ami-efd0428f \
                      --amazonec2-instance-type p2.xlarge \
                      --amazonec2-vpc-id vpc-*** \
                      --amazonec2-access-key AKI*** \
                      --amazonec2-secret-key *** \
                      aws01

# Restart the instance first, to be sure we are running the latest installed kernel
docker-machine restart aws01

# SSH into the machine
docker-machine ssh aws01

# Install official NVIDIA driver package
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo sh -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
sudo apt-get update && sudo apt-get install -y --no-install-recommends linux-headers-generic dkms cuda-drivers

# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb
exit

# Reboot to complete installation of the NVIDIA driver
docker-machine restart aws01

# Environment setup
eval `docker-machine env aws01`
export NV_HOST="ssh://ubuntu@$(docker-machine ip aws01):"
ssh-add ~/.docker/machine/machines/aws01/id_rsa

# Test if docker is using nvidia GPUs
nvidia-docker run — rm nvidia/cuda nvidia-smi

# Install NVIDIA-DOCKER-COMPOSE
sudo pip install nvidia-docker-compose

# COMMANDS TO RUN THE DOCKER IMAGE CONTAINER
nvidia-docker-compose build
nvidia-docker-compose up -d
