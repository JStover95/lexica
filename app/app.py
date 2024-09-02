import dotenv

dotenv.load_dotenv()

import os
from flask import Flask, Response
from app.commands import init_database, drop_database, init_user
from app.extensions import cors, jwt_manager, socketio
from app.utils.logging import logger
from app.views import api, base


def create_app(testing: bool = False) -> Flask:
    if testing:
        flask_config = "Testing"
    else:
        flask_config = os.getenv("FLASK_CONFIG", "Default")

    # set the static folder as the react frontend
    app = Flask(__name__, static_url_path="", static_folder="frontend/build")

    # configure and initialize the app
    app.config.from_object("app.config.%s" % flask_config)
    register_blueprints(app)
    register_commands(app)
    register_extensions(app)

    logger.setLevel(app.config["LOG_LEVEL"])
    for handler in logger.handlers:
        handler.setLevel(app.config["LOG_LEVEL"])

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(base.blueprint)
    app.register_blueprint(api.blueprint)


def register_commands(app: Flask):
    app.cli.add_command(init_database)
    app.cli.add_command(drop_database)
    app.cli.add_command(init_user)


def register_extensions(app: Flask):
    cors.init_app(app)
    jwt_manager.init_app(app)
    socketio.init_app(app)
