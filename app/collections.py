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
    rank: NotRequired[float]


class DictionaryEntry(TypedDict):
    _id: ObjectId
    sourceId: str
    sourceLanguage: str
    writtenForm: str
    variations: list[str]  # TODO: Check whether correct in graphql endpoint
    partOfSpeech: str
    grade: str
    queryStrs: list[str]  # TODO: Check whether correct in graphql endpoint
    senses: NotRequired[list[Sense]]


class SenseRank(TypedDict):
    senseId: ObjectId
    rank: float


class Phrase(TypedDict):
    position: int
    dictionaryEntryIds: list[ObjectId]
    dictionaryEntries: NotRequired[list[DictionaryEntry]]
    senseRanks: NotRequired[list[SenseRank]]
    explanation: str
    contentId: ObjectId


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
    phrases: list[Phrase]
    userId: ObjectId


users: Collection[User] = mongo.db["User"]
senses: Collection[Sense] = mongo.db["Sense"]
dictionary_entries: Collection[DictionaryEntry] = mongo.db["DictionaryEntry"]
contents: Collection[Content] = mongo.db["Content"]
