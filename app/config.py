import os


class Default:
    ENV = "development"
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "secret")
    DEBUG = os.getenv("FLASK_DEBUG", True)
    LOG_LEVEL = os.getenv("FLASK_LOG_LEVEL", "INFO")
    TESTING = False

    COGNITO_REGION = os.getenv("COGNITO_REGION")
    COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
    COGNITO_USERPOOL_ID = os.getenv("COGNITO_USERPOOL_ID")
    COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
    COGNITO_REDIRECT_URI = "http://localhost:3000/"
    COGNITO_JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}/.well-known/jwks.json"


class Production(Default):
    ENV = "production"


class Debug(Default):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class Testing(Default):
    ENV = "development"
    TESTING = True
