# Deep Style Web App

A simple Django web app that schedules and runs neural style on photos.

## Running the program

We need to run the script run_server.sh in order to have docker and nvidia
libraries installed in the AWS instance. This script will also automatically
start the app if it succeeds. If these dependencies have already been installed
and the docker container has already been build, then we can just run:

nvidia-docker-compose build
nvidia-docker-compose up -d

to start the app.

We can check for queued jobs and errors in the js_logger.txt file inside the docker container.

# Acknowledgements
Neural Style Transfer Code - https://github.com/anishathalye/neural-style
