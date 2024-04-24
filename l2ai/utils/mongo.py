import logging
import os
import pymongo

logger = logging.getLogger(__name__)


class Mongo():
    def __init__(self):
        name = os.getenv("MONGO_NAME")
        if name is None:
            logger.info("Environment variable MONGO_NAME is not set. Defaulting to default \"l2ai\"")
            self.name = "l2ai"
        else:
            self.name = name

        host = os.getenv("MONGO_HOST")
        if host is None:
            logger.info("Environment variable MONGO_HOST is not set. Defaulting to default \"localhost\"")
            self.host = "localhost"
        else:
            self.host = host

        port = os.getenv("MONGO_PORT")
        if port is None:
            logger.info("Environment variable MONGO_PORT is not set. Defaulting to default \"27017\"")
            self.port = 27017
        else:
            self.port = int(port)

        self.username  = os.getenv("MONGO_USERNAME")
        if self.username is None:
            logger.warn("Environment variable MONGO_USERNAME is not set. Defaulting to no username.")

        self.password  = os.getenv("MONGO_PASSWORD")
        if self.username is None:
            logger.warn("Environment variable MONGO_USERNAME is not set. Defaulting to no password.")
        
        self.client = pymongo.MongoClient(
            self.host,
            self.port,
            username=self.username,
            password=self.password
        )

    @property
    def db(self):
        return self.client[self.name]
