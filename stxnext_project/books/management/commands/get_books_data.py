from django.core.management.base import BaseCommand
from books.utils import upload_books_for_parameter_to_db


class Command(BaseCommand):
    help = "Fetches books data from Google API"

    def handle(self, *args, **options):
        upload_books_for_parameter_to_db("Hobbit")

        self.stdout.write(
            self.style.SUCCESS(
                "Data has been successfully fetched and saved to a database"
            )
        )
