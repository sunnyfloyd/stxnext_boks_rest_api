from books.models import Book
from books.serializers import BookSerializer
from rest_framework.exceptions import ValidationError


def upload_books_json_to_db(books_json):
    """
    Given a JSON or a Python dict in a Google Books API format upload each item
    to a database using BookSerializer linked to a Book model.

    If an item with a given ID already exists in a database, it will be updated
    with a data from JSON.
    """
    for book in books_json:
        # base fields
        book_data = {
            "id": book["id"],
            "title": book["volumeInfo"]["title"],
            "authors": [author for author in book["volumeInfo"]["authors"]],
            "published_date": parse_incomplete_date(
                book["volumeInfo"]["publishedDate"]
            ),
            "categories": book["volumeInfo"].get("categories", []),
            "average_rating": book["volumeInfo"].get("averageRating", None),
            "ratings_count": book["volumeInfo"].get("ratingsCount", None),
        }

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
