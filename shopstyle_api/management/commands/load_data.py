import json_lines
from pymongo import TEXT

from django.core.management.base import BaseCommand, CommandError

from shopstyle_api.connections import database_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        rows = []
        collection = database_client['products']

        with open('garment_items.jl', 'rb') as f:
            for item in json_lines.reader(f):
                rows.append(item)

        response = collection.insert_many(rows)
        print("Inserted IDs", response.inserted_ids)
        collection.create_index(
            [('product_title', TEXT)],
            default_language='english'
        )
        print("Index created on 'product_title'")