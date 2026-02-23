import pymongo
from flask import current_app, g


def get_db():
    if "db" not in g:
        client = pymongo.MongoClient(current_app.config["MONGODB_URI"])
        g.db = client[current_app.config["MONGO_DB_NAME"]]
    return g.db
