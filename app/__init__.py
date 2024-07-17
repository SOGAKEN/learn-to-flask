from flask import Flask

from app.utils import load_prompts
from config import Config

PROMPTS = load_prompts()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app import routes

    app.register_blueprint(routes.bp)

    return app
