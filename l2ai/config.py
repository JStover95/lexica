import os
import dotenv


class Default:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret")
    DEBUG = os.getenv("FLASK_DEBUG", True)
    LOG_LEVEL = os.getenv("FLASK_LOG_LEVEL", "INFO")
    TESTING = False


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
