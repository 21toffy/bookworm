from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='Test1234'
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_username_validation(self):
        user = User(email='newuser@example.com', username='a', password='Test1234')
        with self.assertRaises(ValidationError):
            user.full_clean()
        user.username = 'abcdefghijk'
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_password_validation(self):
        user = User(email='newuser@example.com', username='newuser', password='weak')
        with self.assertRaises(ValidationError):
            user.full_clean()
        user.password = 'longenoughbutno123'
        with self.assertRaises(ValidationError):
            user.full_clean()
        user.password = 'ValidPassword1'
        user.full_clean()


class UserCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'Test1234'
        }
        self.invalid_payload = {
            'email': 'testuser@example.com',
            'username': 'a',
            'password': 'weak'
        }

    def test_create_valid_user(self):
        response = self.client.post('/api/users/', self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_create_invalid_user(self):
        response = self.client.post('/api/users/', self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
