import click

from grocery.application.factories.grocery_list import GroceryListFactory
from grocery.application.factories.user import UserFactory
from grocery.application.repositories.grocery_list import GroceryListRepository
from grocery.application.repositories.user import UserRepository
from grocery.infrastructure import db
from grocery.infrastructure.db import ResourceConflictError, ResourceNotFoundError


@click.group()
def cli():
    pass


@cli.group()
def user():
    pass


@cli.group()
def glist():
    pass


@user.command(name="create")
@click.option("--name", required=True)
def create_user(name: str):
    service = CreateUserService(username=name)
    user = service.run()
    if user:
        click.echo(f"Succesfully created {user}")
    else:
        click.echo(f"User with name {name} already exists", err=True)


@user.command(name="list")
def list_users(name: str):
    service = ListUsersService()
    users = service.run()
    for user in users:
        click.echo(user)


@user.command(name="get")
@click.option("--name", required=True)
def get_user(name: str):
    try:
        with db.session() as session:
            user = UserRepository(session).get_user_by_name(name)
            click.echo(str(user))
    except ResourceNotFoundError as e:
        click.echo(f"Cannot find user with name: {name}", err=True)


@user.command(name="glist")
@click.option("--name", required=True)
def user_lists(name):
    try:
        with db.session() as session:
            user = UserRepository(session).get_user_by_name(name)
            glists = GroceryListRepository(session).get_lists_for_user(user)
            for glist in glists:
                click.echo(str(glist))
    except ResourceNotFoundError as e:
        click.echo(f"Cannot find user with name: {name}", err=True)


@glist.command(name="create")
@click.option("--name", required=True)
@click.option("--user", required=True)
def create_list(name, user):
    try:
        with db.session() as session:
            user = UserRepository(session).get_user_by_name(user)
            glist = GroceryListFactory.create(name, user)
            repo = GroceryListRepository(session)
            repo.save(glist)
        click.echo(str(glist))
    except ResourceNotFoundError as e:
        click.echo(f"Cannot find user with name: {user}", err=True)


if __name__ == "__main__":
    cli()
