"""
    Test for Post API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core import views

from rest_framework import status
from rest_framework.test import APIClient


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_post(**params):
    return views.Post.objects.create(**params)


POSTS_URL = reverse('post-list')


class PublicPostAPITests(TestCase):
    """Test unauthenticatd API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_to_view_posts(self):
        """Test that auth is required to call the API"""
        response = self.client.get(POSTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostAPITests(TestCase):
    """Test authorized access to APIs"""

    def setUp(self) -> None:
        self.user = create_user(
            username='testuser1',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_auth_required_to_view_posts(self):
        """Test that auth is required to call the List API"""

        other_user = create_user(
            username='testuser2',
            password='testpass123',
        )

        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )

        create_post(
            title="Post 2",
            description="This is Post 2",
            poster=other_user
        )

        response = self.client.get(POSTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))
