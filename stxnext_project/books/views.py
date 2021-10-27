from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from rest_framework import exceptions
from django.core.exceptions import FieldError
from .utils import upload_books_for_parameter_to_db
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


@api_view(["POST"])
def books_update(request):
    """
    Post-only endpoint that allows for uploading new books to a database from
    Google Books API using query parameter.
    """

    q = request.data.get("q")
    if q:
        upload_books_for_parameter_to_db(q)
        return Response(
            {
                "message": "Books database has been successfully updated based on the provided parameter."
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        raise exceptions.ParseError(
            "Books database has been successfully updated based on the provided parameter."
        )
