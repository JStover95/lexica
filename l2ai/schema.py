import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from l2ai import models


class EquivalentType(MongoengineObjectType):
    class Meta:
        model = models.Equivalent


class ContentSurfacesType(MongoengineObjectType):
    class Meta:
        model = models.ContentSurfaces


class ContentIxType(MongoengineObjectType):
    class Meta:
        model = models.ContentIx


class ExplanationType(MongoengineObjectType):
    class Meta:
        model = models.Explanation


class HighlightType(MongoengineObjectType):
    class Meta:
        model = models.Highlight


class SenseRankType(MongoengineObjectType):
    class Meta:
        model = models.SenseRank


class UserType(MongoengineObjectType):
    class Meta:
        model = models.User


class SenseType(MongoengineObjectType):
    class Meta:
        model = models.Sense


class DictionaryEntryType(MongoengineObjectType):
    class Meta:
        model = models.DictionaryEntry


class ContentType(MongoengineObjectType):
    class Meta:
        model = models.Content


class Query(graphene.ObjectType):
    all_users = MongoengineConnectionField(UserType)
    all_dictionary_entries = MongoengineConnectionField(DictionaryEntryType)
    all_senses = MongoengineConnectionField(SenseType)
    all_contents = MongoengineConnectionField(ContentType)

    user_by_id = graphene.Field(UserType, id=graphene.String(required=True))
    dictionary_entry_by_id = graphene.Field(DictionaryEntryType, id=graphene.String(required=True))
    sense_by_id = graphene.Field(SenseType, id=graphene.String(required=True))
    content_by_id = graphene.Field(ContentType, id=graphene.String(required=True))

    def resolve_user_by_id(self, info, id):
        return models.User.objects.get(id=id)

    def resolve_dictionary_entry_by_id(self, info, id):
        return models.DictionaryEntry.objects.get(id=id)

    def resolve_sense_by_id(self, info, id):
        return models.Sense.objects.get(id=id)

    def resolve_content_by_id(self, info, id):
        return models.Content.objects.get(id=id)



class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username):
        user = models.User(username=username)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
