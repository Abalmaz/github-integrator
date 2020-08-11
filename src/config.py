import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    STAGE = False
    TESTING = False
    CSRF_ENABLED = True
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_DATABASE_URI")

    # The folder where the migrations are placed.
    MIGRATE_FOLDER = os.environ.get("MIGRATE_FOLDER")
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_TEST_DATABASE_URI")
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
