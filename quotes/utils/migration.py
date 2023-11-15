import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quoteapp.models import Quotes, Authors, Tag # noqa


client = MongoClient('mongodb://localhost')

db = client.hw

authors = db.authors.find()
quotes = db.quotes.find()

for author in authors:
    Authors.objects.get_or_create(
        fullname=author['fullname'],
        date_born=author['date_born'],
        location_born=author['location_born'],
        bio=author['bio']
    )

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quotes.objects.filter(quote=quote['quote'])))

    if not exist_quote:
        auth = db.authors.find_one({'_id': quote['author']})
        a = Authors.objects.get(fullname=auth['fullname'])
        q = Quotes.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
