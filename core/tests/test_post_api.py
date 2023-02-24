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


def get_post_detail_url(post_id):
    """Helper method to return URL for post details"""
    return reverse('posts', args=[post_id])


POSTS_URL = reverse('posts')


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

    def test_auth_required_to_view_all_posts(self):
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

    def test_auth_required_to_create_post(self):
        """
            Only an authed user can create a new post
            Owner of that post must be the authed user
        """

        new_user = create_user(
            username='testuser2',
            password='testpass123',
        )

        post_payload = {
            'poster': new_user,
            'title': 'New Post',
            'description': 'New Description',
        }

        response = self.client.post(POSTS_URL, post_payload)
        post = views.Post.objects.get(title=response.data['title'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.poster, self.user)
