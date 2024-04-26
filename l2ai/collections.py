from datetime import datetime
from typing import Any, Dict, NotRequired, TypedDict
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult
from l2ai.extensions import mongo

type Ix = list[list[int]]


class Explanation(TypedDict):
    expression: str
    description: str
    definitionIds: list[ObjectId]
    position: int


class ContentSurfaces(TypedDict):
    units: list[str]
    modifiers: list[str]


class ContentIx(TypedDict):
    units: Ix
    modifiers: Ix


class Content(TypedDict):
    _id: ObjectId
    userId: ObjectId
    timestamp: datetime
    method: str
    level: str
    length: str
    format: str
    style: str
    prompt: str
    title: str
    text: str
    surfaces: ContentSurfaces
    ix: ContentIx
    explanationIds: list[Explanation]


class Word(TypedDict):
    _id: ObjectId
    dictId: str
    writtenForm: str
    variations: list[str]
    quertyStrs: list[str]
    partOfSpeech: str
    senseIds: list[ObjectId]


class Sense(TypedDict):
    _id: ObjectId
    ko_KR: str
    en_US: str
    wordId: ObjectId


class Score(TypedDict):
    senseId: ObjectId
    score: int


class User(TypedDict):
    _id: NotRequired[ObjectId]
    lastLogin: NotRequired[datetime]
    username: str
    scores: NotRequired[list[Score]]


contents: Collection[Content] = mongo.db["Content"]
senses: Collection[Sense] = mongo.db["Sense"]
words: Collection[Word] = mongo.db["Word"]
users: Collection[User] = mongo.db["User"]

class Users(Collection):
    name: str = "User"

    # @classmethod
    # def find_one(cls, *args, **kwargs) -> User | None:
    #     return mongo.db[cls.name].find_one(*args, **kwargs)

    # @classmethod
    # def insert_one(cls, document: Dict[str, Any], *args, **kwargs) -> InsertOneResult:
    #     return mongo.db[cls.name].insert_one(document, *args, **kwargs)
