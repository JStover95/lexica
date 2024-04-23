from flask import Flask
from flask_cognito import CognitoAuth
from flask_socketio import SocketIO
import pymongo


class MongoDB():
    def __init__(self, app: Flask | None = None):
        self.app = app
        self.NAME = None
        self.HOST = None
        self.PORT = None
        self.USERNAME = None
        self.PASSWORD = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.NAME = app.config["MONGO_NAME"]
        self.HOST = app.config["MONGO_HOST"]
        self.PORT = app.config["MONGO_PORT"]
        self.USERNAME  = app.config["MONGO_USERNAME"]
        self.PASSWORD  = app.config["MONGO_PASSWORD"]

    @property
    def db(self):
        client = pymongo.MongoClient(
            self.HOST,
            self.PORT,
            username=self.USERNAME,
            password=self.PASSWORD
        )

        return client[self.NAME]


cogauth = CognitoAuth()
mongo = MongoDB()
socketio = SocketIO()


@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user from Cognito JWT payload."""
    return mongo.db["User"].find_one({"email": payload["email"]})
