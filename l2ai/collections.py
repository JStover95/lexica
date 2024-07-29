from datetime import datetime
from typing import NotRequired, TypedDict
from bson.objectid import ObjectId
from pymongo.collection import Collection
from l2ai.extensions import mongo


class User(TypedDict):
    _id: ObjectId
    username: str
    last_login: datetime


class Equivalent(TypedDict):
    language: str
    equivalent: str
    definition: str


class Sense(TypedDict):
    _id: ObjectId
    sense_no: str
    definition: str
    part_of_speech: str
    examples: list[str]
    type: str
    equivalents: list[Equivalent]
    dictionaryEntryId: ObjectId


class DictionaryEntry(TypedDict):
    _id: ObjectId
    source_id: str
    language: str
    written_form: str
    variations: str
    part_of_speech: str
    grade: str
    query_strs: str


class SenseRank(TypedDict):
    rank: float
    senseId: ObjectId


class Highlight(TypedDict):
    position: int
    score: int
    sense_ranks: list[SenseRank]


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
    last_modified: datetime
    method: str
    level: str
    length: str
    format: str
    style: str
    prompt: str
    title: str
    text: str
    # media: file
    surfaces: list[Surfaces]
    ix: list[Ix]
    explanations: list[Explanation]
    highlights: list[Highlight]
    userId: ObjectId


users: Collection[User] = mongo.db["User"]
senses: Collection[Sense] = mongo.db["Sense"]
dictionary_entries: Collection[DictionaryEntry] = mongo.db["DictionaryEntry"]
contents: Collection[Content] = mongo.db["Content"]
