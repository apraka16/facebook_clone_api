"""
    Test for Post API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Post

from rest_framework import status
from rest_framework.test import APIClient

POSTS_URL = reverse('posts')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_post(**params):
    return Post.objects.create(**params)


def get_post_detail_url(post_id):
    """Helper method to return URL for post details"""
    return reverse('post-details', args=[post_id])


def get_users_posts_list_url(poster_id):
    """Helper method to return URL for list of users post"""
    return reverse('user-posts', args=[poster_id])


def get_update_posts_url(post_id):
    """Helper method to return URL for update post API"""
    return reverse('post-update', args=[post_id])


def get_delete_posts_url(post_id):
    """Helper method to return URL for update post API"""
    return reverse('post-delete', args=[post_id])


class PublicPostAPITests(TestCase):
    """Test unauthenticatd API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_to_view_posts(self):
        """Test that auth is required to call the API"""
        response = self.client.get(POSTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_to_retrieve_post_detail(self):
        """Test that auth is required to call retrieve API"""
        self.user = create_user(
            username='testuser1',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )
        # Log out the user forcing unauthentication
        self.client.logout()

        response = self.client.get(get_post_detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_to_update_post_detail(self):
        """Test that auth is required to call update API"""
        self.user = create_user(
            username='testuser1',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )

        # Log out the user forcing unauthentication
        self.client.logout()

        put_payload = {'title': 'Post 2', 'description': 'This is Post 2'}
        response = self.client.put(get_update_posts_url(1), put_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_to_delete_post_detail(self):
        """Test that auth is required to call retrieve API"""
        self.user = create_user(
            username='testuser1',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )

        # Log out the user forcing unauthentication
        self.client.logout()

        response = self.client.put(get_delete_posts_url(1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostAPITests(TestCase):
    """Test authenticated access to APIs"""

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
        post = Post.objects.get(title=response.data['title'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.poster, self.user)

    def test_auth_required_to_view_specific_user_posts(self):
        """Test auth is required to view list of specific user's posts"""
        first_user = get_user_model().objects.get(username='testuser1')

        create_post(poster=self.user, title="Post 1",
                    description="This is Post 1")
        create_post(poster=self.user, title="Post 2",
                    description="This is Post 2")
        create_post(poster=self.user, title="Post 3",
                    description="This is Post 3")

        # Logout with first user
        self.client.logout()

        other_user = create_user(
            username='testuser2',
            password='testpass123',
        )
        # Auth with 2nd user
        self.client.force_authenticate(user=other_user)

        create_post(poster=other_user, title="Post 4",
                    description="This is Post 4")
        create_post(poster=other_user, title="Post 5",
                    description="This is Post 5")

        response = self.client.get(get_users_posts_list_url(first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data))

        # Logout with 2nd user
        self.client.logout()

        # Re-authenticate with first user
        self.client.force_authenticate(user=self.user)

    def test_list_posts_user_does_not_exist_fails_gracefully(self):
        """
            Test posts_per_user fetches all posts if user not found
        """
        create_post(poster=self.user, title="Post 1",
                    description="This is Post 1")
        create_post(poster=self.user, title="Post 2",
                    description="This is Post 2")
        create_post(poster=self.user, title="Post 3",
                    description="This is Post 3")

        # Logout with first user
        self.client.logout()

        other_user = create_user(
            username='testuser2',
            password='testpass123',
        )
        # Auth with 2nd user
        self.client.force_authenticate(user=other_user)

        create_post(poster=other_user, title="Post 4",
                    description="This is Post 4")
        create_post(poster=other_user, title="Post 5",
                    description="This is Post 5")

        response = self.client.get(get_users_posts_list_url(10))

        self.assertEqual(5, len(response.data))

        # Logout with 2nd user
        self.client.logout()

        # Re-authenticate with first user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_post_success(self):
        """
            Test that auth is required to call retrieve API
            Test that called API returns the correct model obj
        """

        for i in range(0, 3):
            title = "Post {i}"
            description = "This is Post {i}"
            create_post(poster=self.user, title=title, description=description)
            response = self.client.get(get_post_detail_url(i+1))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], title)
            self.assertEqual(response.data['description'], description)

    def test_update_own_post_success(self):
        """
            1. Test that auth is required to call update API
            2. Test that API updates/ partially updates the correct model obj &
            fields
        """
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )
        put_payload = {'title': 'Post 2', 'description': 'This is Post 2'}
        response = self.client.put(get_update_posts_url(1), put_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=1).title, put_payload['title'])
        self.assertEqual(Post.objects.get(id=1).description,
                         put_payload['description'])

    def test_partial_update_own_post_success(self):
        """
            1. Test that auth is required to call update API
            2. Test that API updates/ partially updates the correct model obj &
            fields
        """
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )
        patch_payload = {'description': 'This is Post 3'}
        response = self.client.patch(get_update_posts_url(1), patch_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=1).title, 'Post 1')
        self.assertEqual(Post.objects.get(id=1).description,
                         patch_payload['description'])

    def test_update_other_users_post_fails(self):
        """
            1. Test that authed user cannot update other users' posts
        """
        other_user = create_user(
            username='testuser2',
            password='testpass123',
        )
        create_post(
            title="Other Post 1",
            description="This is Other Post 1",
            poster=other_user
        )
        put_payload = {
            'title': 'Other Post 2',
            'description': 'This is Other Post 2'
        }
        response = self.client.put(get_update_posts_url(1), put_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_other_users_post_fails(self):
        """
            1. Test that authed user cannot partial update other users' posts
        """
        other_user = create_user(
            username='testuser2',
            password='testpass123',
        )

        create_post(
            title="Other Post 1",
            description="This is Other Post 1",
            poster=other_user
        )
        patch_payload = {'description': 'This is Other Post 3'}
        response = self.client.patch(get_update_posts_url(1), patch_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_success(self):
        """
            1. Test that auth is required to call delete API
            2. Test that API deletes the correct model obj &
            fields
            3. Test that authed user cannot delete other users' posts
        """
        create_post(
            title="Post 1",
            description="This is Post 1",
            poster=self.user
        )

        response = self.client.delete(get_delete_posts_url(1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
