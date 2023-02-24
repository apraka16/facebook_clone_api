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
    """Helper method to create user"""
    return get_user_model().objects.create_user(**params)


def get_user_detail_url(user_id):
    """Helper method to retrieve user detail"""
    return reverse('user-detail', args=[user_id])


class PublicUserAPITests(TestCase):
    """Test public features of user API"""
    # Set up the client (dummy browser) to call HTTP methods on
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test whether user is created successfully on giving username
        and password"""
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
                'password': 'testpass123'
            },
        ]

        # Create users
        for payload in payloads:
            self.client.post(CREATE_USER_URL, payload)

        # Fetch list of all users
        response = self.client.get(USER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_failure(self):
        """Test retrieving user by unauthed user fails"""
        payload = {
            'username': 'testuser1',
            'password': 'testpass123',
        }

        self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(username='testuser1')

        response = self.client.get(get_user_detail_url(user.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_user_failure(self):
        """Test updating user by unauthed user fails"""
        payload = {
            'username': 'testuser1',
            'password': 'testpass123',
            'first_name': 'test',
            'last_name': 'user1',
            'email': 'testuser1@example.com',
        }

        self.client.post(CREATE_USER_URL, payload)

        put_payload = {
            'username': 'testuser2',
            'password': 'testpass1234',
            'first_name': 'test',
            'last_name': 'user2',
            'email': 'testuser2@example.com',
        }

        user = get_user_model().objects.get(username='testuser1')
        response = self.client.put(get_user_detail_url(user.id), put_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_user_failure(self):
        """Test updating user by unauthed user fails"""
        payload = {
            'username': 'testuser1',
            'password': 'testpass123',
            'first_name': 'test',
            'last_name': 'user1',
            'email': 'testuser1@example.com',
        }

        self.client.post(CREATE_USER_URL, payload)
        patch_payload = {'username': 'testuser2'}
        user = get_user_model().objects.get(username='testuser1')
        response = self.client.patch(
            get_user_detail_url(user.id),
            patch_payload
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_failure(self):
        """Test deleting user by unauthed user fails"""
        payload = {
            'username': 'testuser1',
            'password': 'testpass123',
        }

        self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(username='testuser1')

        response = self.client.delete(get_user_detail_url(user.id))

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
            email='old_email@example.com',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_users_success(self):
        """Test fetching list of all users as authorized"""

        create_user(username='testuser2', password='testpass123')  # 2
        create_user(username='testuser3', password='testpass123')  # 3

        response = self.client.get(USER_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(response.data))

    def test_retrieve_self_detail_success(self):
        """Test retrieving own user detail by authed user passes"""

        response = self.client.get(get_user_detail_url(self.user.id))
        user = get_user_model().objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, self.user.username)

    def test_retrieve_other_user_detail_success(self):
        """Test retrieving other user detail by authed user passes"""

        create_user(
            username='testuser2',
            password='testpass123',
            email='testuser2@example.com'
        )  # 2

        create_user(
            username='testuser3',
            password='testpass123',
            email='testuser2@example.com'
        )  # 3

        user_2 = get_user_model().objects.get(username='testuser2')
        user_3 = get_user_model().objects.get(username='testuser3')

        for k in [user_2, user_3]:
            response = self.client.get(get_user_detail_url(k.id))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(k.username, response.data['username'])
            self.assertEqual(k.email, response.data['email'])

    def test_put_self_user_success(self):
        """Test updating own user detail by authed user passes"""

        put_payload = {
            'username': 'testuser2',
            'password': 'testpass1234',
            'first_name': 'test',
            'last_name': 'user2',
            'email': 'testuser2@example.com',
        }

        response = self.client.put(
            get_user_detail_url(self.user.id),
            put_payload
        )

        user = get_user_model().objects.get(id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, put_payload['username'])
        self.assertEqual(user.first_name, put_payload['first_name'])
        self.assertEqual(user.last_name, put_payload['last_name'])
        self.assertEqual(user.email, put_payload['email'])
        self.assertTrue(user.check_password(put_payload['password']))

    def test_put_other_use_detail_fail(self):
        """Test updating other user detail by authed user fails"""

        create_user(
            username='test2user2',
            password='testpass123',
            first_name='test2',
            last_name='user2',
            email='test2user2@example.com'
        )

        original_user = get_user_model().objects.get(username='test2user2')

        put_payload = {
            'username': 'test3user3',
            'password': 'testpass1234',
            'first_name': 'test3',
            'last_name': 'user3',
            'email': 'testuser2@example.com',
        }

        response = self.client.put(
            get_user_detail_url(original_user.id),
            put_payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_user_success(self):
        """Test updating own user detail by authed user passes"""

        patch_payload = {'username': 'testuser2'}
        response = self.client.patch(
            get_user_detail_url(self.user.id),
            patch_payload
        )
        user = get_user_model().objects.get(id=self.user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, patch_payload['username'])
        self.assertEqual(user.email, self.user.email)

    def test_patch_other_user_fail(self):
        """Test updating own user detail by authed user passes"""
        # To update
        pass

    def test_delete_user_success(self):
        """Test deleting self by authed user passes"""
        user = get_user_model().objects.get(username='testuser1')
        response = self.client.delete(get_user_detail_url(user.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
