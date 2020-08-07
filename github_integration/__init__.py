from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

# The migrate handler
migrate = Migrate()


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Create the config from the config object.
    conf_obj = get_config_obj(config)
    app.config.from_object(conf_obj)

    db.init_app(app)
    migrate.init_app(app, db, directory=app.config["MIGRATE_FOLDER"])

    return app


def get_config_obj(config):
    """Return the config object, based on the current config in the env.

    :param config: The config passed. Will be fetched from the
                   environ or secrets if it isn't set.
    :raise RuntimeError: If no config can be found, or if the
                         config value is invalid.
    :return: Config object for a Flask app.
    """

    from config import get_val
    config_mapper = {
        "prod": "config.ProductionConfig",
        "dev": "config.DevelopmentConfig",
        "testing": "config.TestingConfig"
    }

    # If no config, try to find one
    if not config:
        try:
            config = get_val("APP_SETTINGS")
        except KeyError as e:
            # Raise exception if the setting can't be
            # found in the environment or in the secrets file.
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
