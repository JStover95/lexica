from datetime import datetime
from typing import TypedDict
from bson.objectid import ObjectId
from pymongo.collection import Collection
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
    _id: ObjectId
    lastLogin: datetime
    username: str
    scores: list[Score]


contents: Collection[Content] = mongo.db["Content"]
senses: Collection[Sense] = mongo.db["Sense"]
users: Collection[User] = mongo.db["User"]
words: Collection[Word] = mongo.db["Word"]
