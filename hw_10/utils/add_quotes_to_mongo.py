import json

from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.hw_10


with open("utils\\quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)


for quote in quotes:
    author = db.authors.find_one({"author": quote["author"]})
    if author:
        db.quotes.insert_one(
            {
                "quote": quote["quote"],
                "tags": quote["tags"],
                "author": ObjectId(author["_id"]),
            }
        )
