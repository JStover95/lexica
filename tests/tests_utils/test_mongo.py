from app.utils.logging import logger
from app.utils.mongo import Mongo
from tests.utils import Fake

class TestMongo:
    def test_db(self):
        mongo = Mongo()
        user = mongo.db["User"].find_one()

        assert user is not None
        assert user["username"] == Fake.username(0)
