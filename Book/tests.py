import json
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Book
from User.models import User
from .serializers import BookSerializer

# initialize the APIClient app
client = APIClient()

class BookViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@testmail.com',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.headers = {
            'Authorization': f'Token {self.token.key}'
        }
        Book.objects.create(title='Test Book', author='Test Author', best_seller=True, num_pages=10)

    def test_get_book_by_id(self):
        response = client.get('/book/1/', **self.headers)
        book = Book.objects.get(pk=1)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            "best_seller":True,
            "num_pages":10
        }
        response = client.post('/book/', data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_book_by_id(self):
        response = client.delete('/book/1/', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_update_book_by_id_partially(self):
    #     data = {
    #         'year_published': 2023
    #     }
    #     response = client.patch('/book/1/', data, format='json', **self.headers)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publish_message_to_rabbitmq(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            "best_seller":True,
            "num_pages":10
        }
        response = client.post('/book/', data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = f"New book created: {data['title']} by {data['author']}"
        # Ensure that the message is published to RabbitMQ
        self.assertIn(message, self.rabbitmq_messages)

    def test_process_message_received_from_rabbitmq(self):
        message = 'Test message'
        response = client.post('/book/publish/', {'message': message}, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure that the message is processed correctly
        self.assertEqual(self.processed_message, message)
