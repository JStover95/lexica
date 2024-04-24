import os
import dotenv


class Default:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret")
    DEBUG = os.getenv("FLASK_DEBUG", True)
    LOG_LEVEL = os.getenv("FLASK_LOG_LEVEL", "INFO")
    TESTING = False

    MONGO_NAME = os.getenv("MONGO_NAME", "l2ai")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

class Development(Default):
    ENV = "development"


class Production(Default):
    ENV = "production"


class Debug(Default):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class Testing(Default):
    ENV = "development"
    TESTING = True
