"""
    Test for Post API
"""
from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


POST_URL = reverse('post-list')


class PublicPostAPITests(TestCase):
    """Test unauthenticatd API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that auth is required to call the API"""
        response = self.client.get(POST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostAPITests(TestCase):
    pass


class PublicUserAPITests(TestCase):
    pass


class PrivateUserAPITests(TestCase):
    pass
