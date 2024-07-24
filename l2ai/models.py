from datetime import datetime, UTC
from mongoengine import Document, EmbeddedDocument, DENY, NULLIFY, CASCADE
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    FileField,
    FloatField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)


class User(Document):
    meta = {"indexes": {"fields": ["$username"], "unique": True}}
    username = StringField(required=True, unique=True)
    last_login = DateTimeField()


class DictionaryEntry(Document):
    meta = {"indexes": ["$query_strs"]}
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
    source_id = StringField()
    sense_no = StringField()
    definition = StringField(required=True)
    part_of_speech = StringField()
    examples = ListField(StringField())
    type = StringField()
    equivalents = ListField(EmbeddedDocumentField("Equivalent"))


class Equivalent(EmbeddedDocument):
    language = StringField(required=True)
    equivalent = StringField()
    definition = StringField()


class Content(Document):
    meta = {"indexes": ["$surfaces"]}
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
    surfaces = ListField(
        EmbeddedDocumentField("ContentSurfaces"), required=True
    )

    ix = ListField(EmbeddedDocumentField("ContentIx"), required=True)
    explanations = ListField(EmbeddedDocumentField("Explanation"))
    highlights = ListField(EmbeddedDocument("Highlight"))
    user = ReferenceField("User", required=True, reverse_delete_rule=DENY)


class ContentSurfaces(EmbeddedDocument):
    units = ListField(StringField(), required=True)
    modifiers = ListField(StringField(), required=True)


class ContentIx(EmbeddedDocument):
    units = ListField(ListField(IntField), required=True)
    modifiers = ListField(ListField(IntField), required=True)


class Explanation(EmbeddedDocument):
    expression = StringField(required=True)
    position = IntField(required=True)  # position must be updated if content is edited
    description = StringField(required=True)


class Highlight(EmbeddedDocument):
    position = IntField(required=True)  # position must be updated if content is edited
    score = IntField(choices=(0, 1, 2, 3))
    dictionary_entry = ReferenceField(
        "DictionaryEntry", reverse_delete_rule=NULLIFY
    )

    sense_ranks = ListField(
        EmbeddedDocument("SenseRank"), 
    )


class SenseRank(EmbeddedDocument):
    sense = ReferenceField("Sense", required=True, reverse_delete_rule=CASCADE)
    rank = FloatField(required=True)
