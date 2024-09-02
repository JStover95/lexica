import datetime
import json
import os
import click

from flask.cli import with_appcontext
from tqdm import tqdm

from app.collections import contents, dictionary_entries, senses, User, users
from app.extensions import mecab, mongo
from app.utils.morphs.parse import get_smap_from_morphs


@click.command()
@with_appcontext
def init_database():
    if os.getenv("MONGO_HOST") != "localhost":
        raise RuntimeError("The flask init-database command can only be used when MONGO_HOST is set to localhost.")
    
    # with open("content.json") as f:
    #     content: list[dict] = json.load(f)

    with open("dict.json") as f:
        dictionary: list[dict] = json.load(f)

    # user: User | None = users.find_one()
    # if user is None:
    #     raise RuntimeError("No user present in the database. Run flask init-user before running flask init-database")

    # content_data = []

    # for row in content:
    #     text = row["text"].strip()
    #     morphs = mecab.parse(text)
    #     units, modfs = get_smap_from_morphs(morphs)

    #     content_data.append({
    #         "userId": user["_id"],
    #         "lastModified": datetime.datetime.now(datetime.UTC),
    #         "method": "",
    #         "level": "",
    #         "length": "",
    #         "format": "",
    #         "style": "",
    #         "prompt": "",
    #         "title": row["title"],
    #         "text": text,
    #         "surfaces": {
    #             "units": units["surfaces"],
    #             "modifiers": modfs["surfaces"],
    #         },
    #         "ix": {
    #             "units": units["ix"],
    #             "modifiers": modfs["ix"],
    #         },
    #         "explanations": [],
    #         "highlights": [],
    #     })

    # contents.create_index(["userId", "timestamp"])
    # contents.create_index({"surfaces": "text"})
    # result = contents.insert_many(content_data)

    print("Initializing dictionary...")
    for entry in tqdm(dictionary):
        dictionary_entry = dictionary_entries.insert_one({
            "sourceId": entry["sourceId"],
            "sourceLanguage": entry["sourceLanguage"],
            "writtenForm": entry["writtenForm"],
            "variations": entry["variations"],
            "partOfSpeech": entry["partOfSpeech"],
            "grade": entry["grade"],
            "queryStrs": entry["queryStrs"],
        })
        dictionary_entry_id = dictionary_entry.inserted_id

        for sense in entry["senses"]:
            senses.insert_one({
                "senseNo": sense["senseNo"],
                "definition": sense["definition"],
                "partOfSpeech": sense["partOfSpeech"],
                "examples": sense["examples"],
                "type": sense["type"],
                "equivalents": sense["equivalents"],
                "dictionaryEntryId": dictionary_entry_id,
            })

    dictionary_entries.create_index({"queryStrs": "text"})
    # return result



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

    user = users.insert_one({"username": username})
    click.echo(repr(user))
