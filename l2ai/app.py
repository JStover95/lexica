import dotenv

dotenv.load_dotenv()

import os
from flask import Flask
from l2ai.commands import drop_database, init_user
from l2ai.extensions import cors, socketio
from l2ai.views import base


def create_app(testing: bool = False):
    if testing:
        flask_config = "Testing"

    else:
        flask_config = os.getenv("FLASK_CONFIG", "Development")

    # set the static folder as the react frontend
    app = Flask(__name__, static_url_path="", static_folder="frontend/build")

    # configure and initialize the app
    app.config.from_object("l2ai.config.%s" % flask_config)
    register_blueprints(app)
    register_commands(app)
    register_extensions(app)

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(base.blueprint)


def register_commands(app: Flask):
    app.cli.add_command(drop_database)
    app.cli.add_command(init_user)


def register_extensions(app: Flask):
    socketio.init_app(app)
    cors.init_app(app)
