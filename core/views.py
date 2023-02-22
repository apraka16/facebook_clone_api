from django.contrib.auth.models import User
from .models import UserProfile
from .permissions import UserPermission

from .serializers import (
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
)

from .models import Post

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Users


class UserListAPIView(generics.ListAPIView):
    """Authed users can see list of all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [UserPermission]
    authentication_classes = [TokenAuthentication]


class UserCreateAPIView(generics.CreateAPIView):
    """Anyone can create a user"""
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [UserPermission]
    authentication_classes = [TokenAuthentication]

# Profiles


class ProfileListAPIView(generics.ListAPIView):
    """Authed users can see list of all profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ProfileCreateAPIView(generics.CreateAPIView):
    """Authed users can create their profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Authed users can retrieve/ update/ destoy their profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

# Post


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
