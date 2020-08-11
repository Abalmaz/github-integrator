import os
import sys

from flask_swagger_ui import get_swaggerui_blueprint

from src import create_app
from src.auth.views import auth

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

app = create_app()

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

app.register_blueprint(auth)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
