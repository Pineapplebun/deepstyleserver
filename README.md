# Deep Style Web App

## Current Progress: Step 1, 3, 5

## NOTES

Start thinking about DL/UL for the website and transferring images from server to server.

Create front end and user authentication

Test on multi GPUs on EC2 and Create an EBS with all dependencies installed


## Running the program

We need to run the script run_server.sh in order to have docker and nvidia
libraries installed in the AWS instance. This script will also automatically
start the app if it succeeds. If these dependencies have already been installed
and the docker container has already been build, then we can just run:

nvidia-docker-compose build
nvidia-docker-compose up -d

to start the app.

We can check for queued jobs and errors in the js_logger.txt file.

## Structure

The web app consists of:

1. Django backend with a PostgreSQL database
2. Python job scheduling script
3. Input/Output in Frontend and Backend
4. Dataflow for Neural Style Transfer
5. Docker installation and dependencies

# Acknowledgements
Neural Style Transfer Code - https://github.com/anishathalye/neural-style
