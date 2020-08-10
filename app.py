from flask_swagger_ui import get_swaggerui_blueprint

from github_integration import create_app
from github_integration.auth.routes import auth

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
