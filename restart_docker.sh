docker rm -f dg01 ps01 ng01
nvidia-docker-compose build
nvidia-docker-compose up -d
nvidia-docker-compose logs
