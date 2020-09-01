import os

from flask import Flask
from flask_github import GitHub

from cryptography.fernet import Fernet


key = os.environ.get("SECRET_KEY")
encryption_type = Fernet(key.encode())

github = GitHub()


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Create the config from the config object.
    conf_obj = get_config_obj(config)
    app.config.from_object(conf_obj)
    github.init_app(app)

    return app


def get_config_obj(config):
    """Return the config object, based on the current config in the env.

    :param config: The config passed. Will be fetched from the
                   environ or secrets if it isn't set.
    :raise RuntimeError: If no config can be found, or if the
                         config value is invalid.
    :return: Config object for a Flask app.
    """

    config_mapper = {
        "prod": "config.ProductionConfig",
        "dev": "config.DevelopmentConfig",
        "testing": "config.TestingConfig"
    }

    if not config:
        try:
            config = os.environ.get("APP_SETTINGS")
        except KeyError as e:
            raise RuntimeError(
                "APP_SETTINGS is not defined in the settings") from e

    try:
        # Try to find the environment variable
        obj = config_mapper[config]
    except KeyError as e:
        confs_str = ", ".join(config_mapper.keys())
        raise RuntimeError(
            "The config option must be one of: {0}".format(confs_str)) from e

    return obj
