import pymongo

from django.conf import settings


mongodb_client = pymongo.MongoClient(settings.MONGODB_URL)
database_client = mongodb_client[settings.MONGODB_DATABASE]