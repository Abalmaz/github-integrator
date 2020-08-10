#!/bin/bash

# The path to the project on your machine.
export PROJECT_PATH=~/projects/zigiai

# Where we can find the secrets of the project.
# See `templates/secrets.template.py`.
export SECRETS_PATH=${PROJECT_PATH}/secrets.py

# Tell flask that we are running in debug mode. Required for flask CLI to work.
export FLASK_DEBUG=1