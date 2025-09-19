import graphene
from graphene_django.types import DjangoObjectType
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        feild = "__all__"

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self,info,name=None,email=None):
        user = User(name=name,email=email)
        user.save()
        return CreateUser(user=user)


# def resolve_all_user(root,info):
#     return User.objects.all()


# def resolve_user(root,info,id):
#     return User.objects.get(pk=id)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.String()
    
    user = graphene.Field(UserType)

    def mutate(self,info,id,name=None,email=None):
        user = User.objects.get(pk=id)
        if name:
            user.name = name
        if email:
            user.email = email
        user.save()
        return UpdateUser(user=user)
    

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self,info,id):
        user = User.objects.get(id=id)
        user.delete()

        return DeleteUser(ok=True)


class Mutation(graphene.ObjectType):
    create_User = CreateUser.Field()
    update_user = UpdateUser.Field()
    Delete_User = DeleteUser.Field()
    

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id = graphene.Int(required=True))


    def resolve_all_users(self,info, **kwargs):
        return User.objects.all()
    
    def resolve_user(self,info,id):
        return User.objects.get(id=id)
    



schema = graphene.Schema(query=Query, mutation= Mutation)