import os

SECRET_KEY = ""

SQL_DATABASE_URI = "postgresql://db_user:db_pass@localhost/db"
SQL_TEST_DATABASE_URI = "postgresql://db_user_test:user_pass@localhost/db_test"

# The settings. 'dev' for development. The config option must be one of: prod, dev, testing
APP_SETTINGS = "dev"

PROJECT_PATH = os.environ["PROJECT_PATH"]
MIGRATE_FOLDER = os.path.join(PROJECT_PATH, "migrations")
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""