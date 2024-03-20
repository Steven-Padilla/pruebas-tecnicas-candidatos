from flask import Flask

from src.utils.errors.CustomException import CustomException

# Routes
from .routes import _ExampleRoute
from .routes import UserRoutes
from .routes import WalletRoutes

app = Flask(__name__)

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(_ExampleRoute.main, url_prefix='/example')
    app.register_blueprint(UserRoutes.main, url_prefix='/user')
    app.register_blueprint(WalletRoutes.main, url_prefix='/wallet')

    return app