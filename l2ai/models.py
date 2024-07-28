from datetime import datetime, UTC
from typing import Generic, Type, TypeVar
from mongoengine import (
    Document,
    EmbeddedDocument,
    QuerySet,
    DENY,
    NULLIFY,
    CASCADE
)
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentListField,
    FileField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

U = TypeVar("U", bound=Document)


class QuerySetManager(Generic[U]):
    def __get__(self, instance: object, cls: Type[U]) -> QuerySet[U]:
        return QuerySet(cls, cls._get_collection())


class User(Document):
    meta = {"indexes": {"fields": ["$username"], "unique": True}}
    objects = QuerySetManager["User"]()

    username = StringField(required=True, unique=True)
    last_login = DateTimeField()


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
    senses = ListField(ReferenceField("Sense", reverse_delete_rule=NULLIFY))


class Sense(Document):
    objects = QuerySetManager["Sense"]()

    source_id = StringField()
    sense_no = StringField()
    definition = StringField(required=True)
    part_of_speech = StringField()
    examples = ListField(StringField())
    type = StringField()
    equivalents = EmbeddedDocumentListField("Equivalent")


class Equivalent(EmbeddedDocument):
    objects = QuerySetManager["Equivalent"]()

    language = StringField(required=True)
    equivalent = StringField()
    definition = StringField()


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
    surfaces = EmbeddedDocumentListField("ContentSurfaces", required=True)
    ix = EmbeddedDocumentListField("ContentIx", required=True)
    explanations = EmbeddedDocumentListField("Explanation")
    highlights = EmbeddedDocumentListField("Highlight")
    user = ReferenceField("User", required=True, reverse_delete_rule=DENY)


class ContentSurfaces(EmbeddedDocument):
    objects = QuerySetManager["ContentSurfaces"]()

    units = ListField(StringField(), required=True)
    modifiers = ListField(StringField(), required=True)


class ContentIx(EmbeddedDocument):
    objects = QuerySetManager["ContentIx"]()

    units = ListField(ListField(IntField), required=True)
    modifiers = ListField(ListField(IntField), required=True)


class Explanation(EmbeddedDocument):
    objects = QuerySetManager["Explanation"]()

    expression = StringField(required=True)
    position = IntField(required=True)  # position must be updated if content is edited
    description = StringField(required=True)


class Highlight(EmbeddedDocument):
    objects = QuerySetManager["Highlight"]()

    position = IntField(required=True)  # position must be updated if content is edited
    score = IntField(choices=(0, 1, 2, 3))
    dictionary_entry = ReferenceField(
        "DictionaryEntry", reverse_delete_rule=NULLIFY
    )

    sense_ranks = EmbeddedDocumentListField("SenseRank")


class SenseRank(EmbeddedDocument):
    objects = QuerySetManager["SenseRank"]()

    sense = ReferenceField("Sense", required=True, reverse_delete_rule=CASCADE)
    rank = FloatField(required=True)
