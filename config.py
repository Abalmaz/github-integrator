import importlib
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Import secrets
try:
    _secrets_path = os.environ["SECRETS_PATH"]
except KeyError:
    raise RuntimeError("Could not find 'SECRETS_PATH' in environment")
else:
    secrets = importlib.machinery.SourceFileLoader("secrets",
                                                   _secrets_path).load_module()


def get_val(key, default=None):
    val = os.environ.get(key, None)
    if val is None:
        try:
            val = getattr(secrets, key)
        except AttributeError:
            if default is not None:
                return default
            raise
    return val


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = get_val("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = get_val("SQL_DATABASE_URI")

    # The folder where the migrations are placed.
    MIGRATE_FOLDER = get_val("MIGRATE_FOLDER")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_val("SQL_TEST_DATABASE_URI")
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
