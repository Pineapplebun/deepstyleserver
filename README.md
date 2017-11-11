# Deep Style Web App

## Current Progress: Step 1, 2, 3, 4, 5

## NOTES

Need to change tensorflow script to allow_soft_placement = TRUE to automatically
use an available gpu. Job scheduler handles gpu assignment to each command. (EDIT: May not
be necessary given that the CUDA_VISIBLE_DEVICES is already changed and tensorflow
will automatically distribute based on the available GPU that can be seen.

Django backend assumed to be sqlite3. Need to test on inputs.
How to safely exit out of job scheduling?

Start thinking about creating docker image and DL/UL for the website.

Getting an error executing this command:
python3 neural_style.py --content ../../deepstyleserver/dswebsite/images/circle1.png --styles ../../deepstyleserver/dswebsite/images/top.png --output ../../deepstyleserver/dswebsite/output_images/cc.png

bad allocation 

## Running the program

We need to run the script run_server.sh in order to have docker and nvidia
libraries installed in the AWS instance. This script will also automatically
start the app if it succeeds. If these dependencies have already been installed
and the docker container has already been build, then we can just run:

nvidia-docker run -p 80:80 -d -it deepstyleapp sh /app/start_app_wrapper.sh

to start the app.

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
