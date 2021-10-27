from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
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
            print(authors)


            # zlapac blad z data nie bedaca rokiem (zlapac przez django exception)

            # return queryset.filter(published_date__year=published_date).order_by()
            # return queryset.order_by(sort)
            return queryset.filter(authors__overlap=authors)


            # if car_model is not None:
            #     car_model = car_model.lower()
            #     # Might want to catch not defined car models here and return
            #     # proper message.
            #     return queryset.filter(car_transactions__model=car_model)
        return queryset
