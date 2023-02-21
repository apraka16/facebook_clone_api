from django.contrib.auth.models import User
from .models import UserProfile

from .serializers import (
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
    AuthTokenSerializer,
)

from .models import Post

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class ListUserAPIView(generics.ListAPIView):
    """Authed users can see list of all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CreateUserAPIView(generics.CreateAPIView):
    """Anyone can create a user"""
    serializer_class = UserSerializer


class ListProfileAPIView(generics.ListAPIView):
    """Authed users can see list of all profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CreateProfileAPIView(generics.CreateAPIView):
    """Authed users can create their profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class RetrieveUpdateDestroyProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Authed users can retrieve/ update/ destoy their profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
