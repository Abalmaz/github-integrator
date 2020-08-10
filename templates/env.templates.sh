#!/bin/bash

BASE_PATH=$PWD

export SECRET_KEY=""

export SQL_DATABASE_URI=""
export SQL_TEST_DATABASE_URI="t"

# The settings. 'dev' for development. The config option must be one of: prod, dev, testing
export APP_SETTINGS="dev"

export MIGRATE_FOLDER=${BASE_PATH}/migrations
export GITHUB_CLIENT_ID=""
export GITHUB_CLIENT_SECRET=""
