from rest_framework.test import APITestCase
from books.serializers import BookSerializer
from books.models import Book
from books.utils import upload_books_json_to_db
from django.urls import reverse
from rest_framework import status


class BookSerializerTestCase(APITestCase):
    def setUp(self):
        Book.objects.create(
            id="aaa",
            title="Harry Potter and the Philosopher's Stone",
            authors=["J. K. Rowling"],
            published_date="1997-06-26",
            categories=["fantasy", "magic"],
            average_rating=4.7,
            ratings_count=2375,
            thumbnail="http://books.google.com/books/content?id=ID_4vQAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        Book.objects.create(
            id="aab",
            title="The Black Swan: Second Edition",
            authors=["Nassim Nicholas Taleb"],
            published_date="2010-05-11",
            categories=["Business", "Economics"],
            average_rating=3.5,
            ratings_count=88,
            thumbnail="http://books.google.com/books/content?id=GSBcQVd3MqYC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        Book.objects.create(
            id="aac",
            title="Lun yu",
            authors=["Yutang Lin", "Kangde Tao", "Dafu Yu", "Xunmei Shao"],
            published_date="1994-04-01",
            categories=[],
            average_rating=None,
            ratings_count=None,
            thumbnail="http://books.google.com/books/content?id=ph4wAAAAMAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
        )
        self.dummy_data = {
            "id": "aad",
            "title": "Galazka Jasminu",
            "authors": ["Adam Asnyk"],
            "published_date": "2010-05-11",
            "categories": ["Nature"],
            "average_rating": 2,
            "ratings_count": 1,
            "thumbnail": "",
        }

    def is_valid_after_single_value_change(self, key, value):
        self.dummy_data[key] = value
        serializer = BookSerializer(data=self.dummy_data)
        return serializer.is_valid()

    def test_correct_title(self):
        serializer = BookSerializer(data=self.dummy_data)
        self.assertTrue(serializer.is_valid())

    def test_empty_title_new_instance(self):
        result = self.is_valid_after_single_value_change("title", "")
        self.assertFalse(result)

    def test_empty_title_existing_instance(self):
        book = Book.objects.get(id="aaa")
        book_data = BookSerializer(book).data
        book_data["average_rating"] = ""
        serializer = BookSerializer(instance=book, data=book_data)
        self.assertFalse(serializer.is_valid())

    def test_average_rating_must_be_integer(self):
        result = self.is_valid_after_single_value_change("average_rating", "a")
        self.assertFalse(result)

    def test_average_rating_cannot_be_empty(self):
        result = self.is_valid_after_single_value_change("average_rating", "")
        self.assertFalse(result)

    def test_ratings_count_must_be_integer(self):
        result = self.is_valid_after_single_value_change("ratings_count", "a")
        self.assertFalse(result)

    def test_ratings_count_cannot_be_empty(self):
        result = self.is_valid_after_single_value_change("ratings_count", "")
        self.assertFalse(result)


class BooksUploadTestCase(APITestCase):
    def setUp(self):
        self.dummy_data = {
            "id": "J6XAswEACAAJ",
            "volumeInfo": {
                "title": "Hobbit",
                "authors": ["J. R. R. Tolkien"],
                "publishedDate": "2018",
                "categories": ["Fiction"],
                "averageRating": 4.5,
                "ratingsCount": 24,
            },
            "imageLinks": {
                "thumbnail": "http://books.google.com/books/content?id=rIqOaeTx074C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
            },
        }

    def test_proper_db_additions(self):
        books_data = [
            {k: f"{v}{i}" if k == "id" else v for k, v in self.dummy_data.items()}
            for i in range(100)
        ]
        upload_books_json_to_db(books_data)
        self.assertEqual(Book.objects.count(), 100)

    def test_proper_db_update(self):
        books_data = [
            {k: f"{v}{i}" if k == "id" else v for k, v in self.dummy_data.items()}
            for i in range(100)
        ]
        upload_books_json_to_db(books_data)
        self.dummy_data["volumeInfo"]["title"] = "Update"

        books_data = [
            {k: f"{v}{i}" if k == "id" else v for k, v in self.dummy_data.items()}
            for i in range(50, 150)
        ]
        upload_books_json_to_db(books_data)
        self.assertEqual(Book.objects.count(), 150)
        self.assertEqual(Book.objects.filter(title="Update").count(), 100)


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        Book.objects.create(
            id="aaa",
            title="Harry Potter and the Philosopher's Stone",
            authors=["J. K. Rowling"],
            published_date="1997-06-26",
            categories=["fantasy", "magic"],
            average_rating=4.7,
            ratings_count=2375,
            thumbnail="http://books.google.com/books/content?id=ID_4vQAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )
        Book.objects.create(
            id="aab",
            title="The Black Swan: Second Edition",
            authors=["Nassim Nicholas Taleb"],
            published_date="2010-05-11",
            categories=["Business", "Economics"],
            average_rating=3.5,
            ratings_count=88,
            thumbnail="http://books.google.com/books/content?id=GSBcQVd3MqYC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )
        Book.objects.create(
            id="aac",
            title="Lun yu",
            authors=["Yutang Lin", "Kangde Tao", "Dafu Yu", "Xunmei Shao"],
            published_date="1994-04-01",
            categories=[],
            average_rating=None,
            ratings_count=None,
            thumbnail="http://books.google.com/books/content?id=ph4wAAAAMAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
        )
        Book.objects.create(
            id="aad",
            title="Dummy Title",
            authors=["A. A. Author", "J. K. Rowling", "Kangde Tao"],
            published_date="1997-07-26",
            categories=["testing", "unit testing"],
            average_rating=5.0,
            ratings_count=1,
            thumbnail="http://books.google.com/books/content?id=ID_4vQAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )

    def test_sorting_with_published_date(self):
        # ascending
        url = reverse("books:book-list") + "?sort=published_date"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], "aac")

        # descending
        url = reverse("books:book-list") + "?sort=-published_date"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], "aab")

    def test_filtering_on_published_date(self):
        url = reverse("books:book-list") + "?published_date=1997&sort=-published_date"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], "aad")
        self.assertEqual(response.data[1]["id"], "aaa")

    def test_filtering_on_authors(self):
        # single author
        url = reverse("books:book-list") + "?author=J. K. Rowling&sort=-published_date"
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], "aad")
        self.assertEqual(response.data[1]["id"], "aaa")

        # multiple authors
        url = (
            reverse("books:book-list")
            + "?author=J. K. Rowling&author=Nassim Nicholas Taleb&sort=-published_date"
        )
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], "aab")
        self.assertEqual(response.data[1]["id"], "aad")
        self.assertEqual(response.data[2]["id"], "aaa")

    def test_book_detail(self):
        url = reverse("books:book-detail", kwargs={"pk": "aac"})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], "aac")
        self.assertEqual(response.data["title"], "Lun yu")
