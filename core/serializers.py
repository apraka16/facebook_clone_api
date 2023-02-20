from rest_framework import serializers

from .models import Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Posts model"""
    class Meta:
        model = Post
        fields = ['title', 'description', 'poster']
        read_only_fields = ['id']
