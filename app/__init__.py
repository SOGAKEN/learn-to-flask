from flask import Flask

from .utils import load_prompts_config


def create_app():
    app = Flask(__name__)

    # Load PROMPTS configuration
    app.config["PROMPTS"] = load_prompts_config("prompts.toml")

    # Setup routes and other configurations
    from .routes import bp

    app.register_blueprint(bp)

    return app
