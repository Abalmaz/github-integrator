#!/bin/bash

# The path to the project on your machine.
export PROJECT_PATH=~/projects/zigiai

# Where we can find the secrets of the project.
# See `templates/secrets.template.py`.
export SECRETS_PATH=${PROJECT_PATH}/secrets.py

# Tell flask that we are running in debug mode. Required for flask CLI to work.
export FLASK_DEBUG=1

export SECRET_KEY=""

export SQL_DATABASE_URI="postgresql://db_user:db_pass@localhost/db"
export SQL_TEST_DATABASE_URI="postgresql://db_user_test:user_pass@localhost/db_test"

# The settings. 'dev' for development.
# The config option must be one of: prod, dev, testing
export APP_SETTINGS="dev"

export PROJECT_PATH=os.environ["PROJECT_PATH"]
export MIGRATE_FOLDER=os.path.join(PROJECT_PATH, "migrations")
export GITHUB_CLIENT_ID=""
export GITHUB_CLIENT_SECRET=""
export FERNET_KEY=b''
