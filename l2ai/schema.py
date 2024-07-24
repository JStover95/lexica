import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from l2ai import models


class EquivalentType(MongoengineObjectType):
    class Meta:
        model = models.EquivalentModel


class ContentSurfacesType(MongoengineObjectType):
    class Meta:
        model = models.ContentSurfacesModel


class ContentIxType(MongoengineObjectType):
    class Meta:
        model = models.ContentIxModel


class ExplanationType(MongoengineObjectType):
    class Meta:
        model = models.ExplanationModel


class HighlightType(MongoengineObjectType):
    class Meta:
        model = models.HighlightModel


class SenseRankType(MongoengineObjectType):
    class Meta:
        model = models.SenseRankModel


class UserType(MongoengineObjectType):
    class Meta:
        model = models.UserModel


class SenseType(MongoengineObjectType):
    class Meta:
        model = models.SenseModel


class DictionaryEntryType(MongoengineObjectType):
    class Meta:
        model = models.DictionaryEntryModel


class ContentType(MongoengineObjectType):
    class Meta:
        model = models.ContentModel


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
        return models.UserModel.objects.get(id=id)

    def resolve_dictionary_entry_by_id(self, info, id):
        return models.DictionaryEntryModel.objects.get(id=id)

    def resolve_sense_by_id(self, info, id):
        return models.SenseModel.objects.get(id=id)

    def resolve_content_by_id(self, info, id):
        return models.ContentModel.objects.get(id=id)



class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username):
        user = models.UserModel(username=username)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
