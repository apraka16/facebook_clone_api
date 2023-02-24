from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import (
    UserProfile,
    Post
)

from .permissions import (
    UserPermission,
    PostPermission,
)

from .serializers import (
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

# Users


class UserListAPIView(generics.ListAPIView):
    """Authed users can see list of all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    authentication_classes = [TokenAuthentication]


class UserCreateAPIView(generics.CreateAPIView):
    """Anyone can create a user"""
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
    """Authed user can create post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class PostRetrieveAPIView(generics.RetrieveAPIView):
    """Authed users can retrieve any post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class PostUpdateAPIView(generics.UpdateAPIView):
    """Authed users can update only own posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission]
    authentication_classes = [TokenAuthentication]


class PostDeleteAPIView(generics.DestroyAPIView):
    """Authed users can delete only own posts"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission]
    authentication_classes = [TokenAuthentication]

# User Posts


class UserPostListAPIView(generics.ListAPIView):
    """
    Authed users can see posts posted by specific user
    If user not found, show all posts
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        filtered_user_id = kwargs['poster_id']
        if get_user_model().objects.filter(id=filtered_user_id).exists():
            filtered_user = get_user_model().objects.get(id=filtered_user_id)
            queryset = Post.objects.filter(poster=filtered_user)
        else:
            print('User not found; showing list of all posts')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
