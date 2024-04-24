from flask_cors import CORS
from flask_socketio import SocketIO
from l2ai.utils.cognito import Cognito
from l2ai.utils.mongo import Mongo

cognito = Cognito()

cors = CORS(
    allow_headers=["authorization", "content-type"],
    supports_credentials=True
)

mongo = Mongo()
socketio = SocketIO()
