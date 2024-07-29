import json
import os
import click

from flask.cli import with_appcontext
from mecab import MeCab

from l2ai.extensions import db
from l2ai.models import User


@click.command()
@with_appcontext
def init_database():
    if os.getenv("MONGO_HOST") != "localhost":
        raise RuntimeError("The flask init-database command can only be used when MONGO_HOST is set to localhost.")
    
    mecab = MeCab()

    with open("content.json") as f:
        data: list[dict] = json.load(f)

    user = User.objects.find_one()
    click.echo(user)
    return
    to_insert = []

    for row in data:
        text = row["text"].strip()
        morphs = mecab.parse(text)
        units, modfs = get_smap_from_morphs(morphs)

        to_insert.append({
            "userId": user_id,
            "timestamp": datetime.now(),
            "title": "",
            "prompt": "",
            "text": text,
            "surfaces": {
                "units": units["surfaces"],
                "modifiers": modfs["surfaces"]
            },
            "ix": {
                "units": units["ix"],
                "modifiers": modfs["ix"]
            },
            "explanations": [],
            "translation": row["translation"]
        })

    content = db["content"]
    content.create_index(["userId", "timestamp"])
    content.create_index({"surfaces": "text"})
    result = content.insert_many(to_insert)

    return result



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
        db.drop_database(name)


@click.command()
@click.option("--username", default=None)
@with_appcontext
def init_user(username: str | None):
    username = username or os.getenv("COGNITO_USERNAME")
    if username is None:
        raise ValueError("Either the environment vairable COGNITO_USERNAME or option --username must be set.")

    user = User(username=username)
    user.save()
    click.echo(repr(user))
