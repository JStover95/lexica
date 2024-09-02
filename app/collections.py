from datetime import datetime
from typing import NotRequired, TypedDict
from bson.objectid import ObjectId
from pymongo.collection import Collection
from app.extensions import mongo


class User(TypedDict):
    _id: ObjectId
    username: str
    lastLogin: datetime


class Equivalent(TypedDict):
    equivalentLanguage: str
    equivalent: str
    definition: str


class Sense(TypedDict):
    _id: ObjectId
    senseNo: str
    definition: str
    partOfSpeech: str
    examples: list[str]
    type: str
    equivalents: list[Equivalent]
    dictionaryEntryId: ObjectId


class DictionaryEntry(TypedDict):
    _id: ObjectId
    sourceId: str
    sourceLanguage: str
    writtenForm: str
    variations: list[str]  # TODO: check that correct in graphql endpoint
    partOfSpeech: str
    grade: str
    queryStrs: list[str]  # TODO: check that correct in graphql endpoint


class DictionaryEntryWithSenses(DictionaryEntry):
    senses: list[Sense]


class SenseRank(TypedDict):
    rank: float
    senseId: ObjectId


class Highlight(TypedDict):
    position: int
    score: int
    senseRanks: list[SenseRank]


class Explanation(TypedDict):
    expression: str
    position: int
    description: str


class Surfaces(TypedDict):
    units: list[str]
    modifiers: list[str]


class Ix(TypedDict):
    units: list[list[int]]
    modifiers: list[list[int]]


class Content(TypedDict):
    _id: ObjectId
    lastModified: datetime
    method: str
    level: str
    length: str
    format: str
    style: str
    prompt: str
    title: str
    text: str
    # media: file
    surfaces: Surfaces
    ix: Ix
    explanations: list[Explanation]
    highlights: list[Highlight]
    userId: ObjectId


users: Collection[User] = mongo.db["User"]
senses: Collection[Sense] = mongo.db["Sense"]
dictionary_entries: Collection[DictionaryEntry] = mongo.db["DictionaryEntry"]
contents: Collection[Content] = mongo.db["Content"]
