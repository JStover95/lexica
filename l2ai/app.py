import os
from flask import Flask
from flask_cors import CORS


def create_app(testing=False):
    if testing:
        flask_config = 'Testing'

    else:
        flask_config = os.getenv('FLASK_CONFIG', 'Development')

    # set the static folder as the react frontend
    app = Flask(__name__, static_url_path='', static_folder='frontend/build')

    # configure CORS
    CORS(
      app,
      allow_headers=['authorization', 'content-type', 'x-csrf-token'],
      origins=os.getenv('AWS_CLOUDFRONT_DOMAIN_NAME', '*'),
      supports_credentials=True
    )

    # configure and initialize the app
    app.config.from_object('l2ai.config.%s' % flask_config)
    register_blueprints(app)
    register_commands(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    pass


def register_commands(app):
    pass


def register_extensions(app):
    pass
