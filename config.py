from importlib import machinery
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Import secrets
try:
    _secrets_path = os.environ["SECRETS_PATH"]
except KeyError:
    raise RuntimeError("Could not find 'SECRETS_PATH' in environment")
else:
    secrets = machinery.SourceFileLoader("secrets",
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
    STAGE = False
    TESTING = False
    CSRF_ENABLED = True
    DEBUG = False
    SECRET_KEY = get_val("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = get_val("SQL_DATABASE_URI")

    # The folder where the migrations are placed.
    MIGRATE_FOLDER = get_val("MIGRATE_FOLDER")
    GITHUB_CLIENT_ID = get_val("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = get_val("GITHUB_CLIENT_SECRET")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_val("SQL_TEST_DATABASE_URI")
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
