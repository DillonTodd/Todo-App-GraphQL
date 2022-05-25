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


class TodoInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    completed = graphene.Boolean()


class CreateTodoMutation(graphene.Mutation):
    class Arguments:
        input = TodoInput(required=True)

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, input):
        todo_instance = Todo(
            title = input.title,
            description = input.description,
            completed = input.completed
        )

        todo_instance.save()

        return CreateTodoMutation(todo=todo_instance)


class UpdateTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        input = TodoInput(required=True)

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, input, id):
        todo_instance = Todo.objects.get(id=id)

        if todo_instance:
            todo_instance.title = input.title
            todo_instance.description = input.description
            todo_instance.completed = input.completed

        todo_instance.save()

        return UpdateTodoMutation(todo=todo_instance)


class DeleteTodoMutation(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        input = TodoInput(required=True)

    todo = graphene.Field(TodoType)

    @classmethod
    def mutate(cls, root, info, input, id):
        todo_instance = Todo.objects.get(id=id)
        todo_instance.delete()

        return DeleteTodoMutation(todo=todo_instance)


class Mutation(graphene.ObjectType):
    create_todo_mutation = CreateTodoMutation.Field()
    update_todo_mutation = UpdateTodoMutation.Field()
    delete_todo_mutation = DeleteTodoMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
