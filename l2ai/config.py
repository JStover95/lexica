import os
import dotenv

dotenv.load_dotenv()


class Default:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret")
    DEBUG = os.getenv("FLASK_DEBUG", True)
    LOG_LEVEL = os.getenv("FLASK_LOG_LEVEL", "INFO")
    COGNITO_REGION = os.getenv("AWS_REGION")
    COGNITO_USERPOOL_ID = os.getenv("COGNITO_USERPOOL_ID")
    # COGNITO_APP_CLIENT_ID = 'abcdef123456'
    COGNITO_CHECK_TOKEN_EXPIRATION = True
    COGNITO_JWT_HEADER_NAME = 'X-JWT-Authorization'
    COGNITO_JWT_HEADER_PREFIX = 'Bearer'
    MONGO_NAME = os.getenv("MONGO_NAME", "l2ai")
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

class Development(Default):
    COGNITO_CHECK_TOKEN_EXPIRATION = False
    ENV = "development"


class Production(Default):
    ENV = "production"


class Debug(Default):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class Testing(Default):
    COGNITO_CHECK_TOKEN_EXPIRATION = False
    ENV = "development"
    TESTING = True
