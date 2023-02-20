"""
    Test cases for User Profile APIs
    - List of all profiles
    - Detail of specific profile
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import UserProfile

from rest_framework import status
from rest_framework.test import APIClient

from datetime import date


PROFILE_URL = reverse('profiles')
CREATE_PROFILE_URL = reverse('create-profile')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserProfileAPITests(TestCase):
    """Test for unauthenticated access for APIs"""
    def setUp(self):
        self.client = APIClient()

    def test_list_user_profile(self):
        """Test unauthenticatd API requests"""
        response = self.client.get(PROFILE_URL)

        self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserProfileAPITests(TestCase):
    """Tests for authenticated access for API"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='testuser1', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_list_user_profiles(self):
        """Test whether list of user profile is fetched for authenticated user"""
        UserProfile.objects.create(
            user=self.user,
            dob=date(1987, 1, 1),
            country='South Africa',
            aboutme='I am a lovely person'
        )

        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(UserProfile.objects.all()))

    def test_create_profile_from_auth_user(self):
        """Test profile can only be created for authed user"""
        # Create another profile (which is not authed)

        payload = {
            'dob': date(1987, 1, 1),
            'country': 'South Africa',
            'aboutme': 'I am a lovely person',
        }

        response = self.client.post(CREATE_PROFILE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], get_user_model().objects.get(id=self.user.id).id)
