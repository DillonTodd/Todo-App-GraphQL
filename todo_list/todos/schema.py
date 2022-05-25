import graphene
from graphene_django import DjangoObjectType
from .models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)
    todo = graphene.Field(TodoType, todo_id=graphene.String())

    def resolve_todos(self, info, **kwargs):
        return Todo.objects.all()

    def resolve_todo(self, info, todo_id):
        return Todo.objects.get(id=todo_id)


schema = graphene.Schema(query=Query)
