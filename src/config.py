import os


class Config:
    """
    Contains a different settings to using separate
    configurations for the production server,
    development and testing
    """
    STAGE = False
    TESTING = False
    CSRF_ENABLED = True
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_DATABASE_URI")
    # The folder where the migrations are placed.
    MIGRATE_FOLDER = os.environ.get("MIGRATE_FOLDER")
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")


class DevelopmentConfig(Config):
    """
    Settings to using for the development server
    """
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_DATABASE_URI")
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Settings to using for the tests
    """
    # SQLALCHEMY_DATABASE_URI = os.environ.get("SQL_TEST_DATABASE_URI")
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Settings to using for the production server
    """
    DEBUG = False
    TESTING = False
