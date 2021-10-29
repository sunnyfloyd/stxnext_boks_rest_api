from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books import views

router = DefaultRouter()
router.register("books", views.BookViewSet)

app_name = "books"

urlpatterns = [
    path("db/", views.BooksUpload.as_view()),
    path("", include(router.urls)),
]
