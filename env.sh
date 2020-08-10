#!/bin/bash

# The path to the project on your machine.
export PROJECT_PATH=~/projects/zigiai
export SECRETS_PATH=${PROJECT_PATH}/secrets.py

export SECRET_KEY="qqqqq"

export SQL_DATABASE_URI="postgresql://zigi:123@localhost/zigiai_github"
export SQL_TEST_DATABASE_URI="postgresql://zigi_test:123@localhost/zigiai_github_test"

# The settings. 'dev' for development. The config option must be one of: prod, dev, testing
export APP_SETTINGS="dev"

export PROJECT_PATH=os.environ["PROJECT_PATH"]
export MIGRATE_FOLDER=${PROJECT_PATH}/migrations
export GITHUB_CLIENT_ID="Iv1.4d14e3790ab2274c"
export GITHUB_CLIENT_SECRET="c7f8f88ae9e5461ac7021d7d13bf64aba07dfa5e"