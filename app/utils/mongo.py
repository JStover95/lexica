import os
import pymongo
from pymongo.database import Database
from app.utils.logging import logger


class Mongo():
    """
    A helper class for using MongoDB.

    This class will initialize using the following environment variables. If
    they are not initialized, default values will be used.
     - MONGO_NAME (default: "lexica")
     - MONGO_HOST (default: "localhost")
     - MONGO_PORT (default: 27107)
     - MONGO_USERNAME (default: None)
     - MONGO_PASSWORD (default: None)

    Attributes:
        name (str)
        host (str)
        port (int)
        username (str | None)
        password (str | None)
        client (MongoClient)


    """
    def __init__(self):
        name = os.getenv("MONGO_NAME")
        if name is None:
            logger.info("Environment variable MONGO_NAME is not set. Defaulting to default \"lexica\"")
            self.name = "lexica"
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
    def db(self) -> Database:
        """
        Return the Mongo database defined by Mongo.name.

        Returns:
            Database
        """
        return self.client[self.name]
