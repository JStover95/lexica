from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from mecab import MeCab

from app.utils.mongo import Mongo

cors = CORS(
    # allow_headers=["Authorization", "Content-Type"],
    supports_credentials=True,
    resources={r"/*": {"origins": "http://localhost:3000"}}
)

mecab = MeCab()
mongo = Mongo()
socketio = SocketIO()
jwt_manager = JWTManager()
