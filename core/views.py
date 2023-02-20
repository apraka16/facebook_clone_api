from django.contrib.auth.models import User

from .serializers import (
    PostSerializer,
    UserSerializer
)

from .models import Post

from rest_framework import generics
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
