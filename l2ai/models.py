from datetime import datetime, UTC
import os
import types
from typing import Generic, Type, TypeVar
from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    QuerySet,
    DENY,
    NULLIFY
)
from mongoengine.fields import (
    DateTimeField,
    ListField,
    EmbeddedDocumentField,
    FileField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)
from mongoengine.queryset.queryset import QuerySet

connect(
    "l2ai-mongo",
    password=os.getenv("MONGO_PASSWORD"),
    username=os.getenv("MONGO_USERNAME")
)

QuerySet.__class_getitem__ = types.MethodType(lambda self, x: self, QuerySet)
U = TypeVar("U", bound=Document)


class QuerySetManager(Generic[U]):
    def __get__(self, instance: object, cls: Type[U]) -> QuerySet[U]:
        return QuerySet(cls, cls._get_collection())


class User(Document):
    meta = {"indexes": [{"fields": ["$username"], "unique": True}]}
    objects = QuerySetManager["User"]()

    username = StringField(required=True, unique=True)
    last_login = DateTimeField()


class Equivalent(EmbeddedDocument):
    language = StringField(required=True)
    equivalent = StringField()
    definition = StringField()


class Sense(Document):
    objects = QuerySetManager["Sense"]()
    source_id = StringField()
    sense_no = StringField()
    definition = StringField(required=True)
    part_of_speech = StringField()
    examples = ListField(StringField())
    type = StringField()
    equivalents = ListField(EmbeddedDocumentField(Equivalent))


class DictionaryEntry(Document):
    meta = {"indexes": ["$query_strs"]}
    objects = QuerySetManager["DictionaryEntry"]()
    source = StringField(required=True)
    source_id = StringField(required=True)
    language = StringField(required=True)
    written_form = StringField(required=True)
    variations = StringField()
    part_of_speech = StringField()
    grade = StringField()
    query_strs = StringField(required=True)
    senses = ListField(ReferenceField(Sense, reverse_delete_rule=NULLIFY))


class SenseRank(EmbeddedDocument):
    sense = ReferenceField(Sense, required=True)
    rank = FloatField(required=True)


class Highlight(EmbeddedDocument):
    position = IntField(required=True)  # position must be updated if content is edited
    score = IntField(choices=(0, 1, 2, 3))
    sense_ranks = ListField(EmbeddedDocumentField(SenseRank))


class Explanation(EmbeddedDocument):
    expression = StringField(required=True)
    position = IntField(required=True)  # position must be updated if content is edited
    description = StringField(required=True)


class ContentSurfaces(EmbeddedDocument):
    units = ListField(StringField())
    modifiers = ListField(StringField())


class UnitsIx(EmbeddedDocument):
    ix = ListField(IntField())


class ModifiersIx(EmbeddedDocument):
    ix = ListField(IntField())


class ContentIx(EmbeddedDocument):
    units = ListField(EmbeddedDocumentField(UnitsIx))
    modifiers = ListField(EmbeddedDocumentField(ModifiersIx))


class Content(Document):
    meta = {"indexes": ["$surfaces"]}
    objects = QuerySetManager["Content"]()
    created_on = DateTimeField(default=lambda: datetime.now(UTC), required=True)
    last_modified = DateTimeField(
        default=lambda: datetime.now(UTC), required=True
    )

    method = StringField()
    level = StringField()
    length = StringField()
    format = StringField()
    style = StringField()
    prompt = StringField()
    title = StringField()
    text = StringField(required=True)
    media = FileField()
    surfaces = ListField(EmbeddedDocumentField(ContentSurfaces), required=True)
    ix = ListField(EmbeddedDocumentField(ContentIx), required=True)
    explanations = ListField(EmbeddedDocumentField(Explanation))
    highlights = ListField(EmbeddedDocumentField(Highlight))
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
