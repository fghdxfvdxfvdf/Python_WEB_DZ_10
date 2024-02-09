import os
from pathlib import Path

import django
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent.parent
import sys

sys.path.append(str(BASE_DIR))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_10.settings")
django.setup()

from quotes.models import Authors, Quotes, Tag  # noqa

client = MongoClient("mongodb://localhost:27017")
db = client.hw_10

authors = db.authors.find()
for author_iter in authors:
    try:
        Authors.objects.get_or_create(
            author=author_iter["author"],
            borns=author_iter["borns"],
            borns_location=author_iter["borns_location"],
            descriptions=author_iter["descriptions"],
        )
    except Exception as err:
        print(err)


quotes = db.quotes.find()
for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quotes.objects.filter(quote=quote["quote"])))

    if not exist_quote:
        author = db.authors.find_one({"_id": quote["author"]})
        a = Authors.objects.get(author=author["author"])
        q = Quotes.objects.create(quote=quote["quote"], author=a)
        for tag in tags:
            q.tags.add(tag)
