"""
    Test for User APIs
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('create-user')
USER_LIST_URL = reverse('user-list')
TOKEN_URL = reverse('auth-token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test public features of user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test whether user is created successfully on giving username and password"""
        payload = {
            'username': 'testuser',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists_error(self):
        pass

    def test_list_user_failure(self):
        """Test fetching list of all users not authorised"""
        payloads = [
            {
                'username': 'testuser1',
                'password': 'testpass123'
            },
            {
                'username': 'testuser2',
                'password': 'testpass123'
            },
            {
                'username': 'testuser3',
                'password':'testpass123'
            },
        ]

        # Create users
        for payload in payloads:
            self.client.post(CREATE_USER_URL, payload)

        # Fetch list of all users
        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_for_user(self):
        """Test generate token for valid credentials"""

        user_details = {
            'username': 'testuser2',
            'password': 'testpass123',
        }
        create_user(**user_details)

        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateUserAPITests(TestCase):
    """Test private features of User API"""

    def setUp(self) -> None:
        self.user = create_user(
            username='testuser1',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_users_success(self):
        """Test fetching list of all users as authorized"""

        create_user(username='testuser2', password='testpass123')  #2
        create_user(username='testuser3', password='testpass123')  #3

        response = self.client.get(USER_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data))
