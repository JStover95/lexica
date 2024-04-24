import os
import click
from flask.cli import with_appcontext
from l2ai.extensions import mongo


@click.command()
@click.option("--email", default=None)
@with_appcontext
def init_user(email: str | None):
    email = email or os.getenv("COGNITO_EMAIL")
    user = mongo.db["User"].insert_one({"email": email})
    click.echo(repr(user))
