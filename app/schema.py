from datetime import datetime, UTC

from bson.objectid import ObjectId
from graphene import (
    Boolean,
    DateTime,
    Field,
    Float,
    InputObjectType,
    Int,
    List,
    Mutation,
    ObjectType,
    Schema,
    String
)

from app.collections import contents, dictionary_entries


class User(ObjectType):
    id = String()
    username = String()
    last_login = DateTime()

    @staticmethod
    def from_mongo(document):
        return User(
            id=str(document["_id"]),
            username=document["username"],
            last_login=document["lastLogin"]
        )


class Equivalent(ObjectType):
    equivalent_language = String()
    equivalent = String()
    definition = String()

    @staticmethod
    def from_mongo(document):
        return Equivalent(
            equivalent_language=document["equivalentLanguage"],
            equivalent=document["equivalent"],
            definition=document["definition"]
        )


class Sense(ObjectType):
    id = String()
    sense_no = String()
    definition = String()
    part_of_speech = String()
    examples = List(String)
    type = String()
    equivalents = List(Equivalent)
    dictionary_entry_id = String()

    @staticmethod
    def from_mongo(document):
        return Sense(
            id=str(document["_id"]),
            sense_no=document["senseNo"],
            definition=document["definition"],
            part_of_speech=document["partOfSpeech"],
            examples=document["examples"],
            type=document["type"],
            equivalents=[
                Equivalent.from_mongo(eq) for eq in document["equivalents"]
            ],
            dictionary_entry_id=str(document["dictionaryEntryId"])
        )


class DictionaryEntry(ObjectType):
    id = String()
    source_id = String()
    source_language = String()
    written_form = String()
    variations = String()
    part_of_speech = String()
    grade = String()
    query_strs = String()

    @staticmethod
    def from_mongo(document):
        return DictionaryEntry(
            id=str(document["_id"]),
            source_id=document["sourceId"],
            source_language=document["sourceLanguage"],
            written_form=document["writtenForm"],
            variations=document["variations"],
            part_of_speech=document["partOfSpeech"],
            grade=document["grade"],
            query_strs=document["queryStrs"]
        )


class DictionaryEntryWithSenses(DictionaryEntry):
    senses = List(Sense)

    @staticmethod
    def from_mongo(document):
        return DictionaryEntryWithSenses(
            id=str(document["_id"]),
            source_id=document["sourceId"],
            source_language=document["sourceLanguage"],
            written_form=document["writtenForm"],
            variations=document["variations"],
            part_of_speech=document["partOfSpeech"],
            grade=document["grade"],
            query_strs=document["queryStrs"],
            senses=[Sense.from_mongo(sense) for sense in document["senses"]]
        )


class SenseRank(ObjectType):
    rank = Float()
    sense_id = String()

    @staticmethod
    def from_mongo(document):
        return SenseRank(
            rank=document["rank"],
            sense_id=str(document["senseId"])
        )


class Highlight(ObjectType):
    position = Int()
    score = Int()
    sense_ranks = List(SenseRank)

    @staticmethod
    def from_mongo(document):
        return Highlight(
            position=document["position"],
            score=document["score"],
            sense_ranks=[
                SenseRank.from_mongo(sr) for sr in document["sense_ranks"]
            ]
        )


class Explanation(ObjectType):
    expression = String()
    position = Int()
    description = String()

    @staticmethod
    def from_mongo(document):
        return Explanation(
            expression=document["expression"],
            position=document["position"],
            description=document["description"]
        )


class Surfaces(ObjectType):
    units = List(String)
    modifiers = List(String)

    @staticmethod
    def from_mongo(document):
        return Surfaces(
            units=document["units"],
            modifiers=document["modifiers"]
        )


class Ix(ObjectType):
    units = List(List(Int))
    modifiers = List(List(Int))

    @staticmethod
    def from_mongo(document):
        return Ix(
            units=document["units"],
            modifiers=document["modifiers"]
        )


class Content(ObjectType):
    id = String()
    last_modified = DateTime()
    method = String()
    level = String()
    length = String()
    format = String()
    style = String()
    prompt = String()
    title = String()
    text = String()
    surfaces = List(Surfaces)
    ix = List(Ix)
    explanations = List(Explanation)
    highlights = List(Highlight)
    user_id = String()

    @staticmethod
    def from_mongo(document):
        return Content(
            id=str(document["_id"]),
            last_modified=document["last_modified"],
            method=document["method"],
            level=document["level"],
            length=document["length"],
            format=document["format"],
            style=document["style"],
            prompt=document["prompt"],
            title=document["title"],
            text=document["text"],
            surfaces=[
                Surfaces.from_mongo(surface)
                for surface in document["surfaces"]
            ],
            ix=[Ix.from_mongo(ix) for ix in document["ix"]],
            explanations=[
                Explanation.from_mongo(exp) for exp in document["explanations"]
            ],
            highlights=[
                Highlight.from_mongo(hl) for hl in document["highlights"]
            ],
            user_id=str(document["userId"])
        )


class Query(ObjectType):
    users = List(User)
    senses = List(Sense)
    dictionary_entries = List(DictionaryEntry)
    contents = List(Content)

    def resolve_users(self, info):
        users = users.find()
        return [User.from_mongo(u) for u in users]

    def resolve_senses(self, info):
        senses = senses.find()
        return [Sense.from_mongo(s) for s in senses]

    def resolve_dictionary_entries(self, info):
        entries = dictionary_entries.find()
        return [DictionaryEntry.from_mongo(e) for e in entries]

    def resolve_contents(self, info):
        contents = contents.find()
        return [Content.from_mongo(c) for c in contents]


class ContentSurfacesInput(InputObjectType):
    units = List(String)
    modifiers = List(String)


class ContentIxInput(InputObjectType):
    units = List(List(Int))
    modifiers = List(List(Int))


class ExplanationInput(InputObjectType):
    expression = String()
    position = Int()
    description = String()


class SenseRankInput(InputObjectType):
    rank = Float()
    senseId = String()


class HighlightInput(InputObjectType):
    position = Int()
    score = Int()
    sense_ranks = List(SenseRankInput)


class UpdateContent(Mutation):
    class Arguments:
        id = String(required=True)
        last_modified = DateTime()
        method = String()
        level = String()
        length = String()
        format = String()
        style = String()
        prompt = String()
        title = String()
        text = String()
        surfaces = List(ContentSurfacesInput)
        ix = List(ContentIxInput)
        explanations = List(ExplanationInput)
        highlights = List(HighlightInput)

    ok = Boolean()
    content = Field(lambda: Content)

    def mutate(self, info, id, **kwargs):
        content_id = ObjectId(id)
        updates = {k: v for k, v in kwargs.items() if v is not None}

        if "last_modified" not in updates:
            updates["last_modified"] = datetime.now(UTC)

        result = contents.find_one_and_update(
            {"_id": content_id},
            {"$set": updates},
            return_document=True
        )

        return UpdateContent(content=Content.from_mongo(result), ok=True)


class Mutation(ObjectType):
    update_content = UpdateContent.Field()


schema = Schema(query=Query, mutation=Mutation)
