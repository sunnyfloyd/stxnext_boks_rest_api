from books.models import Book
from books.serializers import BookSerializer
from rest_framework.exceptions import ValidationError
import requests


def upload_books_for_parameter_to_db(q):
    """
    Request a list of books from Google Books API using a provided query parameter
    and upload it to an internal database using BookSerializer linked to a Book model.

    If an item with a given ID already exists in a database, it will be updated
    with data from Google API response.
    """
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={q}")
    books_json = response.json()["items"]

    for book in books_json:
        # base fields
        book_data = {
            "id": book["id"],
            "title": book["volumeInfo"]["title"],
            "published_date": parse_incomplete_date(
                book["volumeInfo"]["publishedDate"]
            ),
            "categories": book["volumeInfo"].get("categories", []),
            "average_rating": book["volumeInfo"].get("averageRating"),
            "ratings_count": book["volumeInfo"].get("ratingsCount"),
        }

        # authors
        try:
            book_data["authors"] = [author for author in book["volumeInfo"]["authors"]]
        except KeyError:
            book_data["authors"] = []

        # thumbnail
        try:
            book_data["thumbnail"] = book["volumeInfo"]["imageLinks"]["thumbnail"]
        except KeyError:
            book_data["thumbnail"] = ""

        # grabbing an instance in case of object udpate
        try:
            instance = Book.objects.get(id=book_data["id"])
        except Book.DoesNotExist:
            instance = None

        serializer = BookSerializer(instance=instance, data=book_data)

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)


def parse_incomplete_date(date_raw):
    """
    Parse incomplete date (missing month or day) so it is accepted by a DateField.
    """
    input_date = date_raw.split("-")
    date = []
    for i in range(3):
        try:
            date.append(input_date[i])
        except IndexError:
            date.append("01")
    return "-".join(date)
