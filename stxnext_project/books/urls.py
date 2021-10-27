from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books import views

router = DefaultRouter()
router.register("", views.BookViewSet)

app_name = "books"

urlpatterns = [
    path("", include(router.urls)),
]
