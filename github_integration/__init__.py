from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_github import GitHub

from cryptography.fernet import Fernet

from flask_swagger_ui import get_swaggerui_blueprint

key = Fernet.generate_key()
encryption_type = Fernet(key)

db = SQLAlchemy()

# The migrate handler
migrate = Migrate()

github = GitHub()

# swagger specific
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "GitHub integration"
    }
)


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Create the config from the config object.
    conf_obj = get_config_obj(config)
    app.config.from_object(conf_obj)

    db.init_app(app)
    migrate.init_app(app, db, directory=app.config["MIGRATE_FOLDER"])
    github.init_app(app)

    from github_integration.auth.routes import auth
    app.register_blueprint(auth)
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

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

    if not config:
        try:
            config = get_val("APP_SETTINGS")
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
