from app.extensions import socketio
from app.utils.logging import logger


@socketio.event
def generate_prompt():
    pass


@socketio.event
def generate_image():
    pass


@socketio.event
def generate_file():
    pass


@socketio.event
def generate_sentences():
    pass
