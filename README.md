# Deep Style Web App

## Current Progress: Step 1, 2, 3, 4, 5

## NOTES

Start thinking about DL/UL for the website and transferring images from server to server.

Getting an error executing this command:
python3 neural_style.py --content ../../deepstyleserver/dswebsite/images/circle1.png --styles ../../deepstyleserver/dswebsite/images/top.png --output ../../deepstyleserver/dswebsite/output_images/cc.png

Resolved by setting the '--width' argument.

## Running the program

We need to run the script run_server.sh in order to have docker and nvidia
libraries installed in the AWS instance. This script will also automatically
start the app if it succeeds. If these dependencies have already been installed
and the docker container has already been build, then we can just run:

nvidia-docker run -p 8000:8000 -d -it deepstyleapp sh /app/start_app_wrapper.sh

to start the app.

We can check for jobs and errors in the js_logger.txt file.

## Structure

The web app consists of:

1. Django backend with a (SQLite?) database
2. Python job scheduling script
3. Input/Output in Frontend and Backend
4. Dataflow for Neural Style Transfer
5. Docker installation and dependencies

## Fahim (1, 3, 4)
Django backend

## Kevin (2, 4, 5)
Job scheduling
