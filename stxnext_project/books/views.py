from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json


class Books(APIView):
    def get(self, request, format=None):
        return Response(requests.get("https://www.googleapis.com/books/v1/volumes?q=Hobbit").json())

