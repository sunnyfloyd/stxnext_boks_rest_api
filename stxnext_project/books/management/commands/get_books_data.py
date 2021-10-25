from django.core.management.base import BaseCommand
import requests
from books.utils import upload_books_json_to_db


class Command(BaseCommand):
    help = "Fetches books data from Google API"

    def handle(self, *args, **options):
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Hobbit")
        books_json = response.json()["items"]
        upload_books_json_to_db(books_json)

        self.stdout.write(
            self.style.SUCCESS(
                "Data has been successfully fetched and saved to a database"
            )
        )
