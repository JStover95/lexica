from graphene import Field, ID, Mutation, ObjectType, Schema, String
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

    user_by_id = Field(User, id=String(required=True))
    dictionary_entry_by_id = Field(DictionaryEntry, id=String(required=True))
    sense_by_id = Field(Sense, id=String(required=True))
    content_by_id = Field(Content, id=String(required=True))

    content_by_user_id = Field(Content, user_id=ID(required=True))
    dictionary_entry_by_written_form = Field(
        DictionaryEntry, written_form=String(required=True)
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



class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)

    user = Field(User)

    def mutate(self, info, username):
        user = models.User(username=username)
        user.save()
        return CreateUser(user=user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()


schema = Schema(query=Query, mutation=Mutation)
