import os
import click
from flask.cli import with_appcontext
from l2ai.extensions import mongo


@click.command()
@click.option("--name", default=None)
@with_appcontext
def drop_database(name: str | None):
    if os.getenv("MONGO_HOST") != "localhost":
        raise RuntimeError("The flask drop-database command can only be used when MONGO_HOST is set to localhost.")

    name = os.getenv("MONGO_NAME", name)
    if name is None:
        raise ValueError("Either the environment vairable MONGO_NAME or option --name must be set.")

    else:
        mongo.client.drop_database(name)


@click.command()
@click.option("--username", default=None)
@with_appcontext
def init_user(username: str | None):
    username = username or os.getenv("COGNITO_USERNAME")
    if username is None:
        raise ValueError("Either the environment vairable COGNITO_USERNAME or option --username must be set.")

    user = mongo.db["User"].insert_one({"username": username})
    click.echo(repr(user))
