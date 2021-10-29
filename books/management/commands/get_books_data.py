from django.core.management.base import BaseCommand
from books.utils import upload_books_json_to_db
import requests


class Command(BaseCommand):
    help = "Fetches books data from Google API"

    def handle(self, *args, **options):
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=Hobbit")
        if response.status_code != 200:
            self.stdout.write(
                self.style.ERROR("Could not fetch data from Google Books API")
            )
        else:
            upload_books_json_to_db(response.json()["items"])

            self.stdout.write(
                self.style.SUCCESS(
                    "Data has been successfully fetched and saved to a database"
                )
            )
