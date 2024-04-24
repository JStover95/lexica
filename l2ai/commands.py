import os
import click
from flask.cli import with_appcontext
import dotenv
from l2ai.extensions import mongo


@click.command("init-user")
@click.option("--email", default=None)
@with_appcontext
def init_user(email: str | None):
    email = email or os.getenv("COGNITO_USERNAME")
    user = mongo.db["User"].insert_one({"email": email})
    click.echo(repr(user))
