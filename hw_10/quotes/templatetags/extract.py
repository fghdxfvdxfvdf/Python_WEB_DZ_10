from pathlib import Path

from bson.objectid import ObjectId
from django import template

BASE_DIR = Path(__file__).resolve().parent.parent.parent
import sys

sys.path.append(str(BASE_DIR))

from quotes.utils import get_mongodb

register = template.Library()


def get_author(id_):
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(id_)})
    return author["author"] if author["author"] else ""


register.filter("author", get_author)
