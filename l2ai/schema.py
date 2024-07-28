from datetime import datetime, UTC
from typing import Optional
from graphene import (
    Boolean,
    DateTime,
    Field,
    Float,
    ID,
    InputObjectType,
    Int,
    List,
    Mutation,
    ObjectType,
    Schema,
    String
)
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from l2ai import models


class Equivalent(MongoengineObjectType):
    class Meta:
        model = models.Equivalent


class ContentSurfaces(MongoengineObjectType):
    class Meta:
        model = models.ContentSurfaces


class ContentIx(MongoengineObjectType):
    class Meta:
        model = models.ContentIx


class Explanation(MongoengineObjectType):
    class Meta:
        model = models.Explanation


class Highlight(MongoengineObjectType):
    class Meta:
        model = models.Highlight


class SenseRank(MongoengineObjectType):
    class Meta:
        model = models.SenseRank


class User(MongoengineObjectType):
    class Meta:
        model = models.User


class Sense(MongoengineObjectType):
    class Meta:
        model = models.Sense


class DictionaryEntry(MongoengineObjectType):
    class Meta:
        model = models.DictionaryEntry


class Content(MongoengineObjectType):
    class Meta:
        model = models.Content


class Query(ObjectType):
    all_users = MongoengineConnectionField(User)
    all_dictionary_entries = MongoengineConnectionField(DictionaryEntry)
    all_senses = MongoengineConnectionField(Sense)
    all_contents = MongoengineConnectionField(Content)

    user_by_id = Field(User, id=String())
    dictionary_entry_by_id = Field(DictionaryEntry, id=String())
    sense_by_id = Field(Sense, id=String())
    content_by_id = Field(Content, id=String())

    content_by_user_id = Field(Content, user_id=ID())
    dictionary_entry_by_written_form = Field(
        DictionaryEntry, written_form=String()
    )

    def resolve_user_by_id(self, info, id):
        return models.User.objects.get(id=id)

    def resolve_dictionary_entry_by_id(self, info, id):
        return models.DictionaryEntry.objects.get(id=id)

    def resolve_sense_by_id(self, info, id):
        return models.Sense.objects.get(id=id)

    def resolve_content_by_id(self, info, id):
        return models.Content.objects.get(id=id)

    def resolve_content_by_user_id(self, info, user_id):
        return models.Content.objects.get(user=user_id)

    def resolve_dictionary_entry_by_written_form(self, info, written_form):
        return models.DictionaryEntry.objects.find(
            {"$text": {"$search": written_form}}
        )


class UserInput(InputObjectType):
    id: str = ID(required=True)
    username: str = String(required=True)
    last_login = DateTime(required=True)


class ContentSurfacesInput(InputObjectType):
    units: list[Optional[str]] = List(String, required=True)
    modifiers: list[Optional[str]] = List(String, required=True)


class ContentIxInput(InputObjectType):
    units: list[list[Optional[int]]] = List(List(Int), required=True)
    modifiers: list[list[Optional[int]]] = List(List(Int), required=True)


class ExplanationInput(InputObjectType):
    expression: str = String(required=True)
    position: int = Int(required=True)
    description: str = String(required=True)


class SenseRankInput(InputObjectType):
    sense: str = ID(required=True)
    rank: float = Float(required=True)


class HighlightInput(InputObjectType):
    position: int = Int(required=True)
    score: Optional[int] = Int()
    dictionary_entry: Optional[str] = ID()
    sense_ranks: Optional[list[Optional[SenseRankInput]]] = List(SenseRankInput)


class ContentInput(InputObjectType):
    id: str = ID(required=True)
    method: Optional[str] = String()
    level: Optional[str] = String()
    length: Optional[str] = String()
    format: Optional[str] = String()
    style: Optional[str] = String()
    prompt: Optional[str] = String()
    title: Optional[str] = String()
    text: Optional[str] = String()
    media: Optional[str] = String()
    surfaces: Optional[list[Optional[ContentSurfacesInput]]] = List(
        ContentSurfacesInput
    )
    ix: Optional[list[Optional[ContentIxInput]]] = List(ContentIxInput)
    explanations: Optional[list[Optional[ExplanationInput]]] = List(
        ExplanationInput
    )
    highlights: Optional[list[Optional[HighlightInput]]] = List(HighlightInput)
    user: str = ID(required=True)


class UpdateContent(Mutation):
    class Arguments:
        content_data = ContentInput(required=True)

    ok = Boolean()
    content = Field(lambda: Content)

    def mutate(root, info, content_data: ContentInput = None):
        content: models.Content = models.Content.objects.get(id=content_data.id)

        if content_data.method is not None:
            content.method = content_data.method
        if content_data.level is not None:
            content.level = content_data.level
        if content_data.length is not None:
            content.length = content_data.length
        if content_data.format is not None:
            content.format = content_data.format
        if content_data.style is not None:
            content.style = content_data.style
        if content_data.prompt is not None:
            content.prompt = content_data.prompt
        if content_data.title is not None:
            content.title = content_data.title
        if content_data.text is not None:
            content.text = content_data.text
        if content_data.media is not None:
            content.media = content_data.media
        if content_data.surfaces is not None:
            content.surfaces = [
                models.ContentSurfaces(**surface)
                for surface in content_data.surfaces
            ]

        if content_data.ix is not None:
            content.ix = [models.ContentIx(**ix) for ix in content_data.ix]
        if content_data.explanations is not None:
            content.explanations = [
                models.Explanation(**explanation)
                for explanation in content_data.explanations
            ]

        if content_data.highlights is not None:
            content.highlights = [
                models.Highlight(
                    position=highlight.position,
                    score=highlight.score,
                    dictionary_entry=highlight.dictionary_entry,
                    sense_ranks=[
                        models.SenseRank(**sense_rank)
                        for sense_rank in highlight.sense_ranks
                    ] if highlight.sense_ranks else []
                ) for highlight in content_data.highlights
            ]

        if content_data.user is not None:
            content.user = content_data.user

        content.last_modified = datetime.now(UTC)
        content.save()

        return UpdateContent(ok=True, content=content)


schema = Schema(query=Query, mutation=Mutation)
