from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from books.models import Book
from books.serializers import BookSerializer
from rest_framework import exceptions
from django.core.exceptions import FieldError
from books.utils import upload_books_json_to_db
from rest_framework.views import APIView
import requests


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint that retrieves a list of books or a single book using its ID.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Get the list of books allowing for additional filtering and sorting.
        """
        queryset = super().get_queryset()
        if self.action == "list":
            published_date = self.request.query_params.get("published_date")
            sort = self.request.query_params.get("sort")
            authors = self.request.query_params.getlist("author")

            try:
                if published_date:
                    queryset = queryset.filter(published_date__year=published_date)
                if authors:
                    queryset = queryset.filter(authors__overlap=authors)
                if sort:
                    queryset = queryset.order_by(sort)
            except FieldError:
                raise exceptions.ParseError(
                    "Provided value by which sorting should be done is not recognizable."
                )
            except ValueError:
                raise exceptions.ParseError(
                    "Value for 'published_date' filter needs to be a number representing a year."
                )
        return queryset


class BooksUpload(APIView):
    """
    Post-only endpoint that allows for uploading new books to a database from
    Google Books API associated with provided 'q' value.
    """

    def post(self, request, format=None):
        q = request.data.get("q")

        if q:
            response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={q}"
            )
            if response.status_code != 200:
                exceptions.server_error(request)
            upload_books_json_to_db(response.json()["items"])
            return Response(
                {
                    "message": "Books database has been successfully updated based on the provided parameter."
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            raise exceptions.ParseError(
                "'q' and its value (it cannot be an empty string) need to be provided in the request's body."
            )
