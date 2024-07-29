import os

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from mongoengine import connect

from l2ai.utils.cognito import Cognito
# from l2ai.utils.mongo import Mongo

cognito = Cognito()

cors = CORS(
    allow_headers=["Authorization", "Content-Type"],
    supports_credentials=True
)

# mongo = Mongo()
db = connect(
    os.getenv("MONGO_NAME"),
    password=os.getenv("MONGO_PASSWORD"),
    username=os.getenv("MONGO_USERNAME")
)

socketio = SocketIO()
jwt_manager = JWTManager()
