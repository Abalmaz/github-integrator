import os
import sys


from flask_swagger_ui import get_swaggerui_blueprint

from src import create_app
from src.auth.views import auth
from src.database import init_db

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

app = create_app()
init_db()

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

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
