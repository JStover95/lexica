from datetime import datetime
from mongoengine import Document, EmbeddedDocument
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


class Equivalent(EmbeddedDocument):
    language = StringField()
    equivalent = StringField()
    definition = StringField()


class Sense(Document):
    meta = {"collection": "sense"}
    target_id = StringField()
    sense_no = StringField()
    definition = StringField()
    part_of_speech = StringField()
    examples = ListField(StringField())
    type = StringField()
    equivalents = ListField(EmbeddedDocumentField(Equivalent))


class DictionaryEntry(Document):
    meta = {"collection": "definition"}
    source = StringField()
    target_id = StringField()
    language = StringField()
    written_form = StringField()
    variations = StringField()
    part_of_speech = StringField()
    grade = StringField()
    query_strs = StringField()
    senses = ListField(ReferenceField(Sense))


class Explanation(EmbeddedDocument):
    expression = StringField()
    description = StringField()
    senses = ListField(ReferenceField(Sense))
    sense_scores = ListField(FloatField())


class ContentSurfaces(EmbeddedDocument):
    units = ListField(StringField())
    modifiers = ListField(StringField())


class ContextIx(EmbeddedDocument):
    units = ListField(ListField(IntField))
    modifiers = ListField(ListField(IntField))


class Content(Document):
    meta = {"collection": "content"}
    user = ReferenceField()
    timestamp = DateTimeField(default=datetime.nowf)
    method = StringField()
    level = StringField()
    length = StringField()
    format = StringField()
    style = StringField()
    prompt = StringField()
    title = StringField()
    text = StringField()
    media = FileField()
    surfaces = ListField(EmbeddedDocumentField(ContentSurfaces))
    ix = ListField(EmbeddedDocumentField(ContextIx))
    explanations = ListField(EmbeddedDocumentField(Explanation))


class Score(EmbeddedDocument):
    sense = ReferenceField(Sense)
    score = IntField()


class User(Document):
    meta = {"collection": "user"}
    username = StringField()
    last_login = DateTimeField()
    scores = ListField(EmbeddedDocumentField(Score))
