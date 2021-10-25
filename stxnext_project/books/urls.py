from django.urls import path, include
from .views import Books

app_name = 'books'

urlpatterns = [
    path("", Books.as_view()),
]
