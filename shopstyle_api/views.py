from rest_framework.views import APIView

from django.http import JsonResponse
from django.conf import settings

from .connections import database_client


class ProductAPIView(APIView):
    def format_response(self, result):
        response = {"data": result}
        return JsonResponse(response)

    def get_query(self):
        q = self.request.query_params.get('q')

        query = { 
            # "product_title": {"$regex" : q}
            '$text': { '$search': q }
        }
        return query

    def get_queryset(self):
        collection = database_client['products']
        offset = self.request.query_params.get('offset', 0)
        limit = self.request.query_params.get('page_size', settings.API_PAGE_SIZE)

        return collection.find(self.get_query()).skip(offset).limit(limit)

    def get(self, request, *args, **kwargs):
        result = []

        for item in self.get_queryset():
            item['id'] = str(item.get('_id'))
            item.pop('_id', '')
            result.append(item)
        
        return self.format_response(result)